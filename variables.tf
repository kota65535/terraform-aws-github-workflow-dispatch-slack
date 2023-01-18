variable "lambda_name" {
  description = "Lambda name"
  type        = string
  default     = "github-workflow-dispatcher"
}

variable "lambda_iam_role_name" {
  description = "Lambda IAM role name"
  type        = string
  default     = "github-workflow-dispatcher"
}

variable "api_gateway_name" {
  description = "API gateway name"
  type        = string
  default     = "github-workflow-dispatcher"
}

variable "github_token" {
  description = "GitHub token"
  type        = string
}

variable "slack_bot_token" {
  description = "Slack bot token"
  type        = string
}

variable "slack_verification_token" {
  description = "Slack verification token"
  type        = string
}
