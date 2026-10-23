import os
import boto3
from mindee import Client
from openai import OpenAI
import deepl
import requests
from pymongo import MongoClient
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def get_azure_document_intelligence_client():
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    return DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )


def get_aws_textract_client():
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client(
        "textract",
        region_name=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )


def get_mindee_client():
    mindee_api_key = os.environ["MINDEE_API_KEY"]
    return Client(mindee_api_key)


def get_openai_client():
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def get_deepl_translator():
    deepl_auth_key = os.environ["DEEPL_AUTH_KEY"]
    return deepl.Translator(deepl_auth_key)


def get_azure_content_safety_headers():
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]
    return {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
        "Endpoint": endpoint,
    }


def get_azure_content_safety_endpoint_url():
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    return f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-01"


def get_mongodb_client():
    mongodb_atlas_uri = os.environ["MONGODB_ATLAS_URI"]
    return MongoClient(mongodb_atlas_uri)
