import os
from google.cloud import pubsub_v1
from google.cloud import translate_v3
from google.cloud import datastore
import google.generativeai as genai

# Google Cloud Project ID
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")

# Pub/Sub Topic and Subscription IDs
PUBLISH_TOPIC_ID = os.getenv("PUBSUB_PUBLISH_TOPIC_ID", "my-publish-topic")
DEAD_LETTER_TOPIC_ID = os.getenv("PUBSUB_DEAD_LETTER_TOPIC_ID", "my-dead-letter-topic")
SUBSCRIPTION_ID = os.getenv("PUBSUB_SUBSCRIPTION_ID", "my-subscription")

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")

# Translation API Location
TRANSLATION_LOCATION = os.getenv("TRANSLATION_LOCATION", "global")


def get_publisher_client():
    """Returns a Google Cloud Pub/Sub PublisherClient."""
    return pubsub_v1.PublisherClient()


def get_subscriber_client():
    """Returns a Google Cloud Pub/Sub SubscriberClient."""
    return pubsub_v1.SubscriberClient()


def get_gemini_model(model_name: str = "gemini-pro"):
    """Returns a Google Gemini GenerativeModel."""
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel(model_name)


def get_translation_client():
    """Returns a Google Cloud TranslationServiceClient."""
    return translate_v3.TranslationServiceClient()


def get_datastore_client():
    """Returns a Google Cloud DatastoreClient."""
    return datastore.Client(project=PROJECT_ID)
