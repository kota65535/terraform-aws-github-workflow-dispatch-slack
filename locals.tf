locals {
  python_version = "3.9"

  terraform_tmp_dir = "${path.root}/.terraform/tmp"
  lambda_zip_path   = "${local.terraform_tmp_dir}/lambda-${var.lambda_name}-${random_string.main.result}.zip"
  layer_zip_path    = "${local.terraform_tmp_dir}/layer-${var.lambda_name}-${random_string.main.result}.zip"
}

data "aws_caller_identity" "self" {}

data "aws_region" "current" {}
