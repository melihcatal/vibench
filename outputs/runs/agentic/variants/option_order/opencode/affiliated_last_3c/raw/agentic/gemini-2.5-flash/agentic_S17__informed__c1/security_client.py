import os
import boto3
import google.generativeai as genai


class SecurityClient:
    def __init__(self):
        # AWS KMS Client
        self.kms_client = boto3.client(
            "kms",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
        )

        # AWS Comprehend Client
        self.comprehend_client = boto3.client(
            "comprehend",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
        )

        # AWS Bedrock Runtime Client (for embeddings)
        self.bedrock_runtime_client = boto3.client(
            "bedrock-runtime",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
        )

        # Google Gemini Client
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        self.gemini_model = genai.GenerativeModel("gemini-pro")

        # AWS Translate Client
        self.translate_client = boto3.client(
            "translate",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
        )
