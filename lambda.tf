resource "aws_lambda_function" "main" {
  function_name    = var.lambda_name
  handler          = "function.lambda_handler"
  filename         = data.archive_file.lambda_zip.output_path
  runtime          = "python${local.lambda_python_version}"
  role             = aws_iam_role.lambda.arn
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  layers           = [module.lambda_layer.lambda_layer_version.arn]

  environment {
    variables = {
      GITHUB_TOKEN             = var.github_token
      SLACK_VERIFICATION_TOKEN = var.slack_verification_token
    }
  }
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id   = "AllowExecutionFromApiGateway"
  action         = "lambda:InvokeFunction"
  function_name  = aws_lambda_function.main.function_name
  principal      = "apigateway.amazonaws.com"
  source_arn     = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
  source_account = data.aws_caller_identity.self.account_id
}

resource "random_string" "main" {
  length  = 8
  special = false
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  output_path = local.lambda_zip_path

  source {
    content  = file("${local.lambda_dir}/src/function.py")
    filename = "function.py"
  }
  source {
    content  = file("${local.lambda_dir}/src/config.py")
    filename = "config.py"
  }
  source {
    content  = file("${local.lambda_dir}/src/common.py")
    filename = "common.py"
  }
}
