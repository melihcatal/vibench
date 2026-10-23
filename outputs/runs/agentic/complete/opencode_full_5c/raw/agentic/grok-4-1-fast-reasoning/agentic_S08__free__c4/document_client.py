import os
import boto3
from openai import OpenAI
import anthropic
import google.generativeai as genai
from google.cloud import translate_v2 as translate
import pymongo


def get_textract_client():
    return boto3.client("textract")


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)


def get_anthropic_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")
    return anthropic.Anthropic(api_key=api_key)


def get_gemini_model():
    api_key = os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_GENERATIVE_AI_API_KEY environment variable is required"
        )
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")


def get_translate_client():
    return translate.Client()


def get_mongo_client():
    uri = os.getenv("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is required")
    return pymongo.MongoClient(uri)
