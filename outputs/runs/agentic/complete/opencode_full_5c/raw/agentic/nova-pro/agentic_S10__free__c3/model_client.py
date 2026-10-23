import os
import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"


def get_api_key():
    return os.getenv("HUGGING_FACE_API_KEY")


def create_headers(api_key):
    return {"Authorization": f"Bearer {api_key}"}


def create_payload(text):
    return {"inputs": text}
