import os
import openai
import anthropic
import cohere
import google.generativeai as genai
from google.cloud import translate_v2 as translate


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    return openai.OpenAI(api_key=api_key)


def get_anthropic_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    return anthropic.Anthropic(api_key=api_key)


def get_cohere_client():
    api_key = os.getenv("COHERE_API_KEY")
    return cohere.Client(api_key=api_key)


def configure_google_genai():
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)


def get_google_translate_client():
    # Assumes GOOGLE_APPLICATION_CREDENTIALS is set in the environment
    return translate.Client()


def get_perspective_api_key():
    return os.getenv("PERSPECTIVE_API_KEY")


def get_elevenlabs_api_key():
    return os.getenv("ELEVENLABS_API_KEY")
