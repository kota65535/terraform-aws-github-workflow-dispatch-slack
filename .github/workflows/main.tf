terraform {
  backend "s3" {
    bucket = "terraform-backend-561678142736"
    region = "ap-northeast-1"
    key    = "terraform-aws-github-workflow-dispatch-slack.tfstate"
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.67.0"
    }
  }
  required_version = "~> 1.5.0"
}

provider "aws" {
  region = "ap-northeast-1"
}

module "workflow_dispatch_slack" {
  source = "../../"

  github_token             = var.github_token
  slack_bot_token          = var.slack_bot_token
  slack_verification_token = var.slack_verification_token
}
