import os
import boto3
from mindee import Client, product

class DocumentAIClient:
    def __init__(self):
        pass

    def get_mindee_client(self) -> Client:
        api_key = os.getenv("MINDEE_API_KEY")
        if not api_key:
            raise ValueError("MINDEE_API_KEY environment variable not set.")
        return Client(api_key=api_key)

    def get_textract_client(self):
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region_name = os.getenv("AWS_REGION_NAME", "us-east-1") # Default region

        if not aws_access_key_id or not aws_secret_access_key:
            raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set.")

        return boto3.client(
            "textract",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region_name
        )

    def get_gemini_client(self):
        import google.generativeai as genai
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-pro")

    def get_deepl_translator(self):
        import deepl
        auth_key = os.getenv("DEEPL_AUTH_KEY")
        if not auth_key:
            raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
        return deepl.Translator(auth_key)

    def get_dynamodb_client(self):
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region_name = os.getenv("AWS_REGION_NAME", "us-east-1")

        if not aws_access_key_id or not aws_secret_access_key:
            raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set for DynamoDB.")
        return boto3.client("dynamodb",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region_name)
