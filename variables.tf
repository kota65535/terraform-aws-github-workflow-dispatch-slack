variable "lambda_name" {
  description = "Lambda name"
  type        = string
  default     = "github-workflow-dispatch-slack"
}

variable "lambda_iam_role_name" {
  description = "Lambda IAM role name"
  type        = string
  default     = "github-workflow-dispatch-slack"
}

variable "api_gateway_name" {
  description = "API gateway name"
  type        = string
  default     = "github-workflow-dispatch-slack"
}

variable "github_token" {
  description = "GitHub token"
  type        = string
}

variable "slack_verification_token" {
  description = "Slack verification token"
  type        = string
}
