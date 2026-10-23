import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
import boto3
import google.generativeai as genai
from azure.ai.contentsafety import ContentSafetyClient
from google.cloud import translate_v2 as translate
import google.cloud.firestore


def get_azure_document_intelligence_client():
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    if not endpoint or not key:
        raise ValueError(
            "Azure Document Intelligence credentials not set in environment variables."
        )
    return DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )


def get_aws_textract_client():
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS Textract credentials not set in environment variables.")
    return boto3.client(
        "textract",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name="us-east-1",
    )


def get_google_gemini_client():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "Google Gemini API key not set in environment variable GOOGLE_API_KEY."
        )
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-pro")


def get_azure_content_safety_client():
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError(
            "Azure AI Content Safety credentials not set in environment variables."
        )
    return ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))


def get_google_cloud_translate_client():
    return translate.Client()


def get_google_firestore_client():
    return google.cloud.firestore.Client()
