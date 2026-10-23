import os
import boto3
import google.generativeai as genai
from google.cloud import translate_v3 as translate
import requests


def get_kms_client():
    # Environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("kms", region_name=aws_region)


def get_gemini_model(model_name: str):
    # Environment variable: GOOGLE_API_KEY
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai.GenerativeModel(model_name)


def get_gemini_embedding_model_name(model_name: str) -> str:
    # Environment variable: GOOGLE_API_KEY
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return model_name  # genai.embed_content takes model as string


def get_translation_client():
    # Environment variable: GOOGLE_APPLICATION_CREDENTIALS (or default ADC)
    return translate.TranslationServiceClient()


def get_perspective_api_config():
    # Environment variable: PERSPECTIVE_API_KEY
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    return {"api_key": api_key, "endpoint": endpoint}
