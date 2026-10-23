import os
from google.cloud import pubsub_v1
from google.cloud import translate_v3 as translate
from google.cloud import firestore
import google.generativeai as genai


# Google Cloud Pub/Sub Client
def get_pubsub_publisher_client():
    return pubsub_v1.PublisherClient()


def get_pubsub_subscriber_client():
    return pubsub_v1.SubscriberClient()


# Google Gemini API Client
def get_gemini_client():
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai.GenerativeModel("gemini-pro")


# Perspective API Client (using requests as it's a REST API)
def get_perspective_api_key():
    return os.environ.get("PERSPECTIVE_API_KEY")


# Google Cloud Translation Client
def get_translation_client():
    return translate.TranslationServiceClient()


# Google Firestore Client
def get_firestore_client():
    return firestore.Client()
