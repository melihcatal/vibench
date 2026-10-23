import os
from google.cloud import pubsub_v1
from google.cloud import firestore
from google.cloud import translate_v3 as translate
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class PubSubClient:
    def __init__(self):
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()


class GeminiClient:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel("gemini-pro")


class FirestoreClient:
    def __init__(self):
        self.db = firestore.Client()


class TranslationClient:
    def __init__(self):
        self.client = translate.TranslationServiceClient()
