import os
import google.cloud.logging
import google.generativeai as genai
from google.cloud import translate_v2 as translate
import requests


def get_logging_client():
    return google.cloud.logging.Client()


def get_gemini_client():
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai


def get_perspective_api_client():
    return os.environ.get("PERSPECTIVE_API_KEY")


def get_translation_client():
    return translate.Client()
