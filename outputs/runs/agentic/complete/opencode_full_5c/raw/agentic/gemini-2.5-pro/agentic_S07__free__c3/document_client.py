import os
import cohere
import openai
import google.generativeai as genai
from google.cloud import vision, translate_v2
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient


def get_google_vision_client() -> vision.ImageAnnotatorClient:
    return vision.ImageAnnotatorClient()


def get_azure_document_intelligence_client() -> DocumentAnalysisClient:
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    return DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))


def get_google_translate_client() -> translate_v2.Client:
    return translate_v2.Client()


def get_google_generative_ai_client() -> genai.GenerativeModel:
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")
    return model


def get_openai_client() -> openai.OpenAI:
    return openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_cohere_client() -> cohere.Client:
    return cohere.Client(os.getenv("COHERE_API_KEY"))
