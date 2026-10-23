import os
import boto3

AWS_REGION = "YOUR_AWS_REGION"
COGNITO_CLIENT_ID = "YOUR_COGNITO_CLIENT_ID"


def get_cognito_client():
    return boto3.client("cognito-idp", region_name=AWS_REGION)


def get_translate_client():
    return boto3.client("translate", region_name=AWS_REGION)


def get_comprehend_client():
    return boto3.client("comprehend", region_name=AWS_REGION)


def get_bedrock_client():
    return boto3.client("bedrock-runtime", region_name=AWS_REGION)


def get_dynamodb_client():
    return boto3.client("dynamodb", region_name=AWS_REGION)
