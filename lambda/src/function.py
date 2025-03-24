import base64
import copy
import json
import logging
from typing import TypedDict, Dict
from urllib.parse import parse_qs

import requests
from requests import HTTPError

import common
from common import GitHubClient
from config import Config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

config = Config()


class SlackVerificationError(Exception):
    pass


class SlackInteractionAction(TypedDict):
    action_id: str
    value: str


class SlackInteractionPayload(TypedDict):
    type: str
    user: dict
    token: str
    channel: dict
    message: dict
    actions: list[SlackInteractionAction]
    response_url: str


class WorkflowDispatcherRequest(TypedDict):
    owner: str
    repo: str
    workflow_id: str
    ref: str
    inputs: dict


class ActionValue(TypedDict, total=False):
    choice: bool
    request: WorkflowDispatcherRequest


# Lambda function entrypoint
def lambda_handler(event: Dict, context):
    logger.info(f"Input: {json.dumps(event)}")
    # Parse message
    body = parse_qs(base64.b64decode(event["body"]).decode())
    payload: SlackInteractionPayload = json.loads(body["payload"][0])
    logger.info(f"Payload: {json.dumps(payload)}")

    # Check verification token
    verify_token(payload["token"])

    value: ActionValue = json.loads(payload["actions"][0]["value"])

    if value["choice"]:
        dispatch_workflow(value)

    update_message(payload["message"], payload["user"]["id"], payload["response_url"], value["choice"])


def verify_token(token):
    if isinstance(token, list):
        token = token[0]
    if token != config.slack_verification_token:
        raise SlackVerificationError(f"Verification token not matched. Given: {token}")


def dispatch_workflow(value: ActionValue):
    req: WorkflowDispatcherRequest = value["request"]

    client = GitHubClient(config.github_token)

    if "ref" in req:
        ref = req["ref"]
    else:
        repo = client.get_repo(req["owner"], req["repo"])
        ref = repo["default_branch"]

    if "inputs" in req:
        inputs = req["inputs"]
    else:
        inputs = {}

    client.dispatch_workflow(
        req["owner"],
        req["repo"],
        req["workflow_id"],
        common.DispatchWorkflowRequest(ref, inputs))


def update_message(message, user_id, response_url, choice):
    message = copy.deepcopy(message)

    # Append result text
    if choice:
        text = f"👍 Approved by <@{user_id}>."
    else:
        text = f"❌ Cancelled by <@{user_id}>."

    for i, a in enumerate(message["attachments"]):
        for j, b in enumerate(a["blocks"]):
            if b["type"] == "actions":
                message["attachments"][i]["blocks"][j] = {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": text
                    }
                }

    # Respond to the user
    res = requests.post(response_url,
                        json={
                            "replace_original": "false",
                            "text": message["text"],
                            "blocks": message["blocks"],
                            "attachments": message["attachments"]
                        })
    try:
        res.raise_for_status()
    except HTTPError as e:
        logger.error(f"Request failed: status={e.response.status_code}, body=${e.response.text}")
