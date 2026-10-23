import os
from google.cloud import pubsub_v1
from google.cloud import firestore
from google.cloud import translate
import google.generativeai as genai

# Google Cloud Pub/Sub
def get_pubsub_publisher_client():
    return pubsub_v1.PublisherClient()

def get_pubsub_subscriber_client():
    return pubsub_v1.SubscriberClient()

# Google Cloud Firestore
def get_firestore_client():
    return firestore.Client()

# Google Cloud Translation
def get_translate_client():
    return translate.TranslationServiceClient()

# Google Gemini API
def configure_gemini():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set for Gemini API.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')
