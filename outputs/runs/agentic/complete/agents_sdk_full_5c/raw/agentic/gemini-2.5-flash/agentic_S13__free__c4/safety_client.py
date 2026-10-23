# safety_client.py
# This file provides local configuration and client helper utilities for Text Content Safety.
# It can be used to initialize clients for various providers or manage common settings.

import os
import openai
import boto3
import vertexai

class SafetyClient:
    def __init__(self, project_id: str = None, location: str = None):
        self._project_id = project_id or os.environ.get("GCP_PROJECT_ID")
        self._location = location or os.environ.get("GCP_LOCATION", "us-central1")

        # Initialize Vertex AI
        if self._project_id and self._location:
            vertexai.init(project=self._project_id, location=self._location)
        
        # OpenAI API Key is typically managed via environment variable by the SDK
        # AWS credentials are typically managed via environment variables or IAM roles by boto3

    def get_vertexai_model(self, model_name: str = "gemini-pro"):
        from vertexai.preview.generative_models import GenerativeModel
        return GenerativeModel(model_name)

    def get_openai_client(self):
        return openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def get_aws_comprehend_client(self):
        return boto3.client(
            'comprehend',
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
        )

    def get_aws_polly_client(self):
        return boto3.client(
            'polly',
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
        )

    def get_aws_ssm_client(self):
        return boto3.client(
            'ssm',
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
        )

    def get_google_translation_client(self):
        from google.cloud import translate_v3
        return translate_v3.TranslationServiceClient()

