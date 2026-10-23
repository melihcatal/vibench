import os
import boto3
from google.cloud import vision
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import cohere
import anthropic
import openai


def get_google_vision_client():
    return vision.ImageAnnotatorClient()


def get_textract_client():
    return boto3.client(
        "textract",
        region_name=os.environ.get("AWS_REGION"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )


def get_form_recognizer_client():
    endpoint = os.environ.get("AZURE_FORM_RECOGNIZER_ENDPOINT")
    key = os.environ.get("AZURE_FORM_RECOGNIZER_KEY")
    return DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))


def get_google_translate_client():
    from google.cloud import translate_v2 as translate

    return translate.Client()


def get_cohere_client():
    return cohere.Client(os.environ.get("COHERE_API_KEY"))


def get_anthropic_client():
    return anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def get_openai_client():
    return openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
