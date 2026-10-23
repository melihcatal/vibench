import os
from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient
from azure.monitor.query import LogsQueryClient
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
from azure.translator.text import TextTranslationClient, TranslatorCredential


def get_logs_ingestion_client(endpoint: str) -> LogsIngestionClient:
    credential = DefaultAzureCredential()
    return LogsIngestionClient(endpoint=endpoint, credential=credential)


def get_logs_query_client() -> LogsQueryClient:
    credential = DefaultAzureCredential()
    return LogsQueryClient(credential=credential)


def get_content_safety_client(endpoint: str, key: str) -> ContentSafetyClient:
    return ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_text_analytics_client(endpoint: str, key: str) -> TextAnalyticsClient:
    return TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_azure_openai_client(azure_endpoint: str, api_key: str, api_version: str) -> AzureOpenAI:
    return AzureOpenAI(
        azure_endpoint=azure_endpoint,
        api_key=api_key,
        api_version=api_version
    )

def get_translator_client(endpoint: str, region: str, key: str) -> TextTranslationClient:
    return TextTranslationClient(endpoint=endpoint, credential=TranslatorCredential(key, region))
