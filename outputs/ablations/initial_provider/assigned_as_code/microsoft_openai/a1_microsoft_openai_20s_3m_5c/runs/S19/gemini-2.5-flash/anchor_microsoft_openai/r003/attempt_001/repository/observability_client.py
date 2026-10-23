import os
from azure.identity import DefaultAzureCredential
from azure.monitor.query import MetricsQueryClient
from azure.ai.textanalytics import TextAnalyticsClient
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.storage.blob import BlobServiceClient

def get_metrics_query_client():
    credential = DefaultAzureCredential()
    return MetricsQueryClient(credential=credential)

def get_text_analytics_client(endpoint: str, key: str):
    credential = DefaultAzureCredential()
    return TextAnalyticsClient(endpoint=endpoint, credential=credential)

def get_translator_client(endpoint: str, key: str, region: str):
    credential = DefaultAzureCredential()
    return TextTranslationClient(endpoint=endpoint, credential=credential, region=region)

def get_blob_service_client(account_url: str):
    credential = DefaultAzureCredential()
    return BlobServiceClient(account_url=account_url, credential=credential)
