import os
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any
from azure.identity import DefaultAzureCredential

# Azure Monitor Logs Ingestion API related environment variables
AZURE_LOG_ANALYTICS_WORKSPACE_ID = os.environ.get("AZURE_LOG_ANALYTICS_WORKSPACE_ID")
AZURE_LOG_ANALYTICS_DATA_COLLECTION_ENDPOINT = os.environ.get("AZURE_LOG_ANALYTICS_DATA_COLLECTION_ENDPOINT")
AZURE_LOG_ANALYTICS_DCR_IMMUTABLE_ID = os.environ.get("AZURE_LOG_ANALYTICS_DCR_IMMUTABLE_ID")
AZURE_LOG_ANALYTICS_STREAM_NAME = os.environ.get("AZURE_LOG_ANALYTICS_STREAM_NAME", "Custom-MyApplicationLogs")

# OpenAI API related environment variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1") # For Azure OpenAI, this will be different
OPENAI_ORGANIZATION = os.environ.get("OPENAI_ORGANIZATION")

# Google Cloud Translation API related environment variables
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") # Path to service account key file
GOOGLE_CLOUD_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")


class AzureMonitorClient:
    def __init__(self):
        if not all([AZURE_LOG_ANALYTICS_WORKSPACE_ID, AZURE_LOG_ANALYTICS_DATA_COLLECTION_ENDPOINT, AZURE_LOG_ANALYTICS_DCR_IMMUTABLE_ID]):
            raise ValueError("Azure Monitor environment variables not set. Please set AZURE_LOG_ANALYTICS_WORKSPACE_ID, AZURE_LOG_ANALYTICS_DATA_COLLECTION_ENDPOINT, and AZURE_LOG_ANALYTICS_DCR_IMMUTABLE_ID.")
        self.workspace_id = AZURE_LOG_ANALYTICS_WORKSPACE_ID
        self.data_collection_endpoint = AZURE_LOG_ANALYTICS_DATA_COLLECTION_ENDPOINT
        self.dcr_immutable_id = AZURE_LOG_ANALYTICS_DCR_IMMUTABLE_ID
        self.stream_name = AZURE_LOG_ANALYTICS_STREAM_NAME
        self.credential = DefaultAzureCredential()

    def _get_bearer_token(self):
        # Acquire a token for the Azure Monitor Logs Ingestion API scope
        # The scope for Logs Ingestion API is "https://monitor.azure.com/.default"
        token = self.credential.get_token("https://monitor.azure.com/.default")
        return token.token

    def ingest_logs(self, log_entries: List[Dict[str, Any]], log_stream_name: str = "Custom-MyApplicationLogs"):
        if not log_entries:
            return

        ingestion_url = (
            f"{self.data_collection_endpoint}/dataCollectionRules/{self.dcr_immutable_id}/streams/{log_stream_name}?api-version=2023-01-01"
        )
        headers = {
            "Authorization": f"Bearer {self._get_bearer_token()}",
            "Content-Type": "application/json"
        }

        response = requests.post(ingestion_url, headers=headers, json=log_entries)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        print(f"Successfully ingested {len(log_entries)} logs to Azure Monitor.")

    def query_logs(self, kusto_query: str, timespan_minutes: int = 60) -> List[Dict[str, Any]]:
        # Azure Monitor Query API endpoint
        query_url = f"https://api.loganalytics.io/v1/workspaces/{self.workspace_id}/query"
        headers = {
            "Authorization": f"Bearer {self._get_bearer_token()}",
            "Content-Type": "application/json"
        }
        payload = {
            "query": kusto_query,
            "timespan": timedelta(minutes=timespan_minutes).total_seconds()
        }

        response = requests.post(query_url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        
        # Parse the results - the 'tables' array contains the data
        results = []
        if "tables" in data and len(data["tables"]) > 0:
            table = data["tables"][0]
            columns = [col["name"] for col in table["columns"]]
            for row in table["rows"]:
                results.append(dict(zip(columns, row)))
        return results

class OpenAIClient:
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        self.api_key = OPENAI_API_KEY
        self.api_base = OPENAI_API_BASE
        self.organization = OPENAI_ORGANIZATION

    def _get_headers(self):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        if self.organization:
            headers["OpenAI-Organization"] = self.organization
        return headers

    def summarize_text(self, text: str, model: str = "gpt-3.5-turbo", max_tokens: int = 150) -> str:
        url = f"{self.api_base}/chat/completions"
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                {"role": "user", "content": f"Summarize the following text:\n\n{text}"}
            ],
            "max_tokens": max_tokens
        }
        response = requests.post(url, headers=self._get_headers(), json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    def check_safety(self, text: str) -> Dict[str, Any]:
        url = f"{self.api_base}/moderations"
        payload = {
            "input": text
        }
        response = requests.post(url, headers=self._get_headers(), json=payload)
        response.raise_for_status()
        return response.json()["results"][0]

    def get_embedding(self, text: str, model: str = "text-embedding-ada-002") -> List[float]:
        url = f"{self.api_base}/embeddings"
        payload = {
            "input": text,
            "model": model
        }
        response = requests.post(url, headers=self._get_headers(), json=payload)
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]

class GoogleTranslateClient:
    def __init__(self):
        if not GOOGLE_APPLICATION_CREDENTIALS or not GOOGLE_CLOUD_PROJECT_ID:
            raise ValueError("Google Cloud Translation environment variables not set. Please set GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT_ID.")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS
        from google.cloud import translate_v2 as translate
        self.translate_client = translate.Client(project=GOOGLE_CLOUD_PROJECT_ID)

    def translate_text(self, text: str, target_language: str) -> str:
        result = self.translate_client.translate(text, target_language=target_language)
        return result["translatedText"]
