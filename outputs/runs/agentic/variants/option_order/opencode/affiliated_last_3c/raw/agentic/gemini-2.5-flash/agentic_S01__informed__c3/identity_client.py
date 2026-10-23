import os
import boto3


class IdentityClient:
    def __init__(self):
        self.region = os.environ.get("AWS_REGION", "us-east-1")
        self.user_pool_id = os.environ.get("AWS_COGNITO_USER_POOL_ID")
        self.client_id = os.environ.get("AWS_COGNITO_CLIENT_ID")

        if not self.user_pool_id or not self.client_id:
            raise ValueError(
                "AWS_COGNITO_USER_POOL_ID and AWS_COGNITO_CLIENT_ID must be set"
            )

        self.cognito_idp_client = boto3.client("cognito-idp", region_name=self.region)
        self.translate_client = boto3.client("translate", region_name=self.region)
        self.comprehend_client = boto3.client("comprehend", region_name=self.region)
        self.bedrock_runtime_client = boto3.client(
            "bedrock-runtime", region_name=self.region
        )
        self.dynamodb_client = boto3.client("dynamodb", region_name=self.region)

    def get_cognito_idp_client(self):
        return self.cognito_idp_client

    def get_translate_client(self):
        return self.translate_client

    def get_comprehend_client(self):
        return self.comprehend_client

    def get_bedrock_runtime_client(self):
        return self.bedrock_runtime_client

    def get_dynamodb_client(self):
        return self.dynamodb_client

    def get_user_pool_id(self):
        return self.user_pool_id

    def get_client_id(self):
        return self.client_id
