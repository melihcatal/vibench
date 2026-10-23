import os
from google.cloud import documentai_v1 as documentai
import boto3
import google.generativeai as genai
from google.cloud import translate_v2 as translate
from google.cloud import firestore
import requests


def get_documentai_client():
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
    return documentai.DocumentProcessorServiceClient()


def get_textract_client():
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY should be set in the environment
    return boto3.client("textract", region_name="us-east-1")  # Specify a region


def get_gemini_client():
    # GOOGLE_API_KEY should be set in the environment
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai.GenerativeModel("gemini-pro")


def get_perspective_client():
    # PERSPECTIVE_API_KEY should be set in the environment
    return os.environ.get(
        "PERSPECTIVE_API_KEY"
    )  # API key is directly used in the request, not a client object


def get_translate_client():
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
    return translate.Client()


def get_firestore_client():
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment
    return firestore.Client()
