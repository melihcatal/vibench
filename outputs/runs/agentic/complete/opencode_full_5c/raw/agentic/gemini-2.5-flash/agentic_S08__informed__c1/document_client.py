import os
from mindee import Client, product
from google.cloud import documentai_v1beta3 as documentai
import google.generativeai as genai
from google.cloud import translate_v2 as translate
from google.cloud import firestore


def get_mindee_client():
    api_key = os.environ.get("MINDEE_API_KEY")
    if not api_key:
        raise ValueError("MINDEE_API_KEY environment variable not set.")
    return Client(api_key=api_key)


def get_documentai_client():
    return documentai.DocumentProcessorServiceClient()


def get_gemini_client():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-pro")


def get_google_translate_client():
    return translate.Client()


def get_firestore_client():
    return firestore.Client()
