terraform {
  backend "s3" {
    bucket = "terraform-backend-561678142736"
    region = "ap-northeast-1"
    key    = "terraform-aws-github-workflow-dispatch-slack.tfstate"
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.91.0"
    }
  }
  required_version = "~> 1.11.0"
}

provider "aws" {
  region = "ap-northeast-1"
}

module "workflow_dispatch_slack" {
  source = "../../"

  github_token             = var.github_token
  slack_verification_token = var.slack_verification_token
}
