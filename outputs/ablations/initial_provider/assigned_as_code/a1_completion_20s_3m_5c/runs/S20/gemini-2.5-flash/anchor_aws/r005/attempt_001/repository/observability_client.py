import os

import boto3
import google.generativeai as genai
from google.cloud import translate_v2 as translate


def get_aws_cloudwatch_client(region_name: str):
    return boto3.client("logs", region_name=region_name)


def get_gemini_model(model_name: str):
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    return genai.GenerativeModel(model_name)


def get_translate_client():
    return translate.Client()
