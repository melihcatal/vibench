import os
from google.cloud import pubsub_v1
from google.cloud import translate_v3beta1 as translate
from google.cloud import firestore
import google.generativeai as genai
import httpx  # For Azure AI Content Safety
from dotenv import load_dotenv

load_dotenv()


# Google Cloud Pub/Sub client
def get_pubsub_publisher_client():
    return pubsub_v1.PublisherClient()


def get_pubsub_subscriber_client():
    return pubsub_v1.SubscriberClient()


# Google Gemini API client
def get_gemini_client():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    return genai.GenerativeModel("gemini-pro")


# Azure AI Content Safety client (using httpx for REST API)
def get_azure_content_safety_client():
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set."
        )
    return httpx.Client(base_url=endpoint, headers={"Ocp-Apim-Subscription-Key": key})


# Google Cloud Translation client
def get_translation_client():
    return translate.TranslationServiceClient()


# Google Firestore client
def get_firestore_client():
    return firestore.Client()
