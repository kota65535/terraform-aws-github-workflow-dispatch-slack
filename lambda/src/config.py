import os


class Config:
    github_token: str
    slack_verification_token: str

    def __init__(self):

        # GitHub token. Must have 'repo' scope.
        self.github_token = os.getenv("GITHUB_TOKEN")

        # Slack bot verification token.
        self.slack_verification_token = os.getenv("SLACK_VERIFICATION_TOKEN")
