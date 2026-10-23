import os

from huggingface_hub import InferenceClient

HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(token=HF_TOKEN)


def get_client():
    return client


def normalize_payload(payload):
    return payload


def parse_response(response):
    return response
