import dataclasses
import logging
from dataclasses import dataclass

import requests
from requests import HTTPError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@dataclass
class DispatchWorkflowRequest:
    ref: str
    inputs: dict


class GitHubClient:
    base_url = "https://api.github.com"

    def __init__(self, token):
        self.token = token

    # cf. https://docs.github.com/en/rest/repos/repos#get-a-repository
    def get_repo(self, owner, repo):
        res = requests.get(f"{GitHubClient.base_url}/repos/{owner}/{repo}",
                            headers={
                                "Accept": "application/vnd.github+json",
                                "Authorization": f"token {self.token}"
                            })
        try:
            res.raise_for_status()
        except HTTPError as e:
            logger.error(f"Request failed: status={e.response.status_code}, body=${e.response.text}")
            raise e
        return res.json()

    # cf. https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event
    def dispatch_workflow(self, owner, repo, workflow_id, data: DispatchWorkflowRequest):
        res = requests.post(f"{GitHubClient.base_url}/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches",
                            headers={
                                "Accept": "application/vnd.github+json",
                                "Authorization": f"token {self.token}"
                            },
                            json=dataclasses.asdict(data))
        try:
            res.raise_for_status()
        except HTTPError as e:
            logger.error(f"Request failed: status={e.response.status_code}, body=${e.response.text}")
            raise e
        # 204 No Content
