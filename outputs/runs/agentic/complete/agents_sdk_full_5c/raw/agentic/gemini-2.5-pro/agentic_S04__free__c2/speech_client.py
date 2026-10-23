import os
import assemblyai
import cohere
import deepl
import openai

def get_assemblyai_client():
    """Initializes and returns the AssemblyAI client."""
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
    return assemblyai.Transcriber()

def get_cohere_client():
    """Initializes and returns the Cohere client."""
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    return cohere.Client(api_key)

def get_deepl_client():
    """Initializes and returns the DeepL client."""
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
    return deepl.Translator(auth_key)

def get_openai_client():
    """Initializes and returns the OpenAI client."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return openai.OpenAI(api_key=api_key)

# Centralized clients for easy import in other modules
assemblyai_client = get_assemblyai_client()
cohere_client = get_cohere_client()
deepl_client = get_deepl_client()
openai_client = get_openai_client()
