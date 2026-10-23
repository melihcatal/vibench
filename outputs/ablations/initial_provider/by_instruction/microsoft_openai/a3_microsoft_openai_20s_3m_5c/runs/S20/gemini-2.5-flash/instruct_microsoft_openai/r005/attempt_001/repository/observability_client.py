import os
import requests
import datetime
import hmac
import hashlib
import base64
import json
from openai import AzureOpenAI
from azure.identity import ClientSecretCredential

class ObservabilityClient:
    def __init__(self):
        self.log_analytics_workspace_id = os.environ.get("LOG_ANALYTICS_WORKSPACE_ID")
        self.log_analytics_shared_key = os.environ.get("LOG_ANALYTICS_SHARED_KEY")
        self.log_analytics_api_version = "2016-04-03"
        self.log_analytics_endpoint = f"https://{self.log_analytics_workspace_id}.ods.opinsights.azure.com/api/logs"
        self.log_analytics_query_endpoint = f"https://api.loganalytics.io/v1/workspaces/{self.log_analytics_workspace_id}/query"

        self.azure_openai_api_key = os.environ.get("AZURE_OPENAI_API_KEY")
        self.azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        self.azure_openai_api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2023-05-15")
        self.azure_openai_deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-35-turbo")
        self.azure_openai_embedding_deployment_name = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME", "text-embedding-ada-002")

        self.openai_client = None
        if self.azure_openai_api_key and self.azure_openai_endpoint:
            self.openai_client = AzureOpenAI(
                api_key=self.azure_openai_api_key,
                api_version=self.azure_openai_api_version,
                azure_endpoint=self.azure_openai_endpoint
            )

        self.log_query_credential = None
        self.log_query_client_id = os.environ.get("AZURE_MONITOR_CLIENT_ID")
        self.log_query_client_secret = os.environ.get("AZURE_MONITOR_CLIENT_SECRET")
        self.log_query_tenant_id = os.environ.get("AZURE_MONITOR_TENANT_ID")

        if self.log_query_client_id and self.log_query_client_secret and self.log_query_tenant_id:
            self.log_query_credential = ClientSecretCredential(
                tenant_id=self.log_query_tenant_id,
                client_id=self.log_query_client_id,
                client_secret=self.log_query_client_secret
            )

    def _build_auth_header(self, content_length: int, date: str):
        string_to_sign = f"POST\n{content_length}\napplication/json\nx-ms-date:{date}\n/api/logs"
        bytes_to_sign = string_to_sign.encode("utf-8")
        decoded_key = base64.b64decode(self.log_analytics_shared_key)
        signature = base64.b64encode(hmac.new(decoded_key, bytes_to_sign, digestmod=hashlib.sha256).digest()).decode("utf-8")
        return f"SharedKey {self.log_analytics_workspace_id}:{signature}"

    def post_log_event(self, log_type: str, json_data: list, timestamp_field: str = "") -> requests.Response:
        if not self.log_analytics_workspace_id or not self.log_analytics_shared_key:
            raise ValueError("LOG_ANALYTICS_WORKSPACE_ID and LOG_ANALYTICS_SHARED_KEY must be set.")

        body = json.dumps(json_data)
        content_length = len(body)
        rfc1123date = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        authorization = self._build_auth_header(content_length, rfc1123date)

        headers = {
            "Content-Type": "application/json",
            "Authorization": authorization,
            "Log-Type": log_type,
            "x-ms-date": rfc1123date,
            "time-generated-field": timestamp_field
        }

        response = requests.post(
            f"{self.log_analytics_endpoint}?api-version={self.log_analytics_api_version}",
            data=body,
            headers=headers
        )
        response.raise_for_status()
        return response

    def query_logs(self, query: str, timespan: str) -> dict:
        if not self.log_query_credential:
             raise ValueError("Azure AD credentials (AZURE_MONITOR_CLIENT_ID, AZURE_MONITOR_CLIENT_SECRET, AZURE_MONITOR_TENANT_ID) must be set for querying.")

        token = self.log_query_credential.get_token("https://api.loganalytics.io/.default")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token.token}",
        }

        body = {
            "query": query,
            "timespan": timespan
        }

        response = requests.post(self.log_analytics_query_endpoint, headers=headers, json=body)
        response.raise_for_status()
        return response.json()