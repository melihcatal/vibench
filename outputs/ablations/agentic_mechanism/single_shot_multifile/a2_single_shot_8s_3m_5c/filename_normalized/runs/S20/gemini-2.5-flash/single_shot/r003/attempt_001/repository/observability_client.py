import os
import boto3
from google.cloud import logging_v2
from datadog_api_client.v2 import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
import openai
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
import cohere

class ObservabilityClients:
    def __init__(self):
        self._gcp_logging_client = None
        self._aws_logs_client = None
        self._datadog_logs_api = None
        self._openai_client = None
        self._azure_content_safety_client = None
        self._aws_translate_client = None
        self._cohere_client = None

    @property
    def gcp_logging_client(self):
        if self._gcp_logging_client is None:
            self._gcp_logging_client = logging_v2.Client()
        return self._gcp_logging_client

    @property
    def aws_logs_client(self):
        if self._aws_logs_client is None:
            self._aws_logs_client = boto3.client(
                "logs",
                region_name=os.getenv("AWS_REGION", "us-east-1")
            )
        return self._aws_logs_client

    @property
    def datadog_logs_api(self):
        if self._datadog_logs_api is None:
            configuration = Configuration()
            configuration.api_key["appKeyAuth"] = os.getenv("DATADOG_APP_KEY")
            configuration.api_key["apiKeyAuth"] = os.getenv("DATADOG_API_KEY")
            api_client = ApiClient(configuration)
            self._datadog_logs_api = LogsApi(api_client)
        return self._datadog_logs_api

    @property
    def openai_client(self):
        if self._openai_client is None:
            self._openai_client = openai.OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )
        return self._openai_client

    @property
    def azure_content_safety_client(self):
        if self._azure_content_safety_client is None:
            endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
            key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
            if not endpoint or not key:
                raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set for Azure Content Safety client.")
            self._azure_content_safety_client = ContentSafetyClient(
                endpoint, AzureKeyCredential(key)
            )
        return self._azure_content_safety_client

    @property
    def aws_translate_client(self):
        if self._aws_translate_client is None:
            self._aws_translate_client = boto3.client(
                "translate",
                region_name=os.getenv("AWS_REGION", "us-east-1")
            )
        return self._aws_translate_client

    @property
    def cohere_client(self):
        if self._cohere_client is None:
            self._cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))
        return self._cohere_client

clients = ObservabilityClients()
