import os
import openai
import boto3
from google.cloud import translate_v2 as translate
import cohere
import elevenlabs
import google.generativeai as genai


def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    return openai.Client(api_key=api_key)


def get_comprehend_client():
    return boto3.client(
        "comprehend",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )


def get_google_translate_client():
    return translate.Client()


def get_cohere_client():
    api_key = os.environ.get("COHERE_API_KEY")
    return cohere.Client(api_key)


def get_elevenlabs_client():
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    elevenlabs.set_api_key(api_key)
    return elevenlabs


def configure_google_genai():
    api_key = os.environ.get("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    return genai
