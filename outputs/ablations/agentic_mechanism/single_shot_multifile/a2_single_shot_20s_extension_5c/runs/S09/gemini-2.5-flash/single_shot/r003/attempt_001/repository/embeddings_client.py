import os
from openai import OpenAI, AzureOpenAI
import cohere
import google.generativeai as genai
import anthropic

def get_openai_client() -> OpenAI:
    """Returns an initialized OpenAI client."""
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_cohere_client() -> cohere.Client:
    """Returns an initialized Cohere client."""
    return cohere.Client(api_key=os.environ.get("COHERE_API_KEY"))

def configure_google_genai():
    """Configures Google Generative AI with the API key."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def get_azure_openai_client() -> AzureOpenAI:
    """Returns an initialized Azure OpenAI client."""
    return AzureOpenAI(
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),  
        api_version="2023-05-15", # or newer, check your deployment
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT")
    )

def get_anthropic_client() -> anthropic.Anthropic:
    """Returns an initialized Anthropic client."""
    return anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))