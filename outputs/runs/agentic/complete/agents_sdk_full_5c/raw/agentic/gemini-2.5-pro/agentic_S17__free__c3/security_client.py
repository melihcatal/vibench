import os
import boto3
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
import googleapiclient.discovery
import cohere
import requests
import base64

class KmsClient:
    def __init__(self, region_name: str = None):
        self.region_name = region_name or os.environ.get("AWS_REGION")
        if not self.region_name:
            raise ValueError("AWS region must be provided")
        self.client = boto3.client("kms", region_name=self.region_name)

    def get_client(self):
        return self.client

class DatadogClient:
    def __init__(self):
        self.configuration = Configuration()
        if not self.configuration.api_key.get("apiKeyAuth"):
             raise ValueError("DATADOG_API_KEY environment variable not set")
        if not self.configuration.api_key.get("appKeyAuth"):
            raise ValueError("DATADOG_APP_KEY environment variable not set")
        
        self.api_client = ApiClient(self.configuration)
        self.logs_api = LogsApi(self.api_client)

    def get_logs_api(self):
        return self.logs_api

class PerspectiveClient:
    def __init__(self):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        self.client = googleapiclient.discovery.build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=api_key,
            static_discovery=False,
        )

    def get_client(self):
        return self.client

class CohereClient:
    def __init__(self):
        api_key = os.environ.get("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY environment variable not set")
        self.client = cohere.Client(api_key)

    def get_client(self):
        return self.client

class DeepLClient:
    def __init__(self):
        self.api_key = os.environ.get("DEEPL_API_KEY")
        if not self.api_key:
            raise ValueError("DEEPL_API_KEY environment variable not set")
        self.base_url = "https://api-free.deepl.com/v2/translate"

    def translate(self, text: str, target_lang: str):
        payload = {
            "auth_key": self.api_key,
            "text": text,
            "target_lang": target_lang,
        }
        response = requests.post(self.base_url, data=payload)
        response.raise_for_status()
        return response.json()

kms_client = KmsClient()
datadog_client = DatadogClient()
perspective_client = PerspectiveClient()
cohere_client = CohereClient()
deepl_client = DeepLClient()
