import os
import openai
import cohere
import google.generativeai as genai
from google.cloud import translate_v2 as translate
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    return openai.OpenAI(api_key=api_key)


def get_cohere_client():
    api_key = os.getenv("COHERE_API_KEY")
    return cohere.Client(api_key)


def get_google_generativeai_client():
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    return genai


def get_google_translate_client():
    return translate.Client()


def get_azure_content_safety_client():
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    return ContentSafetyClient(endpoint, AzureKeyCredential(key))
