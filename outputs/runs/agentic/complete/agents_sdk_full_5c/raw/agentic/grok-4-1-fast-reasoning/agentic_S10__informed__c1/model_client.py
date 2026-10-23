import os

def get_mistral_client():
    from mistralai import Mistral
    api_key = os.getenv('MISTRAL_API_KEY')
    if not api_key:
        raise ValueError('MISTRAL_API_KEY environment variable is required.')
    return Mistral(api_key=api_key)

def get_anthropic_client():
    from anthropic import Anthropic
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError('ANTHROPIC_API_KEY environment variable is required.')
    return Anthropic(api_key=api_key)

def get_gemini_client():
    import google.generativeai as genai
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError('GOOGLE_API_KEY environment variable is required.')
    genai.configure(api_key=api_key)
    return genai

def get_openai_client():
    from openai import OpenAI
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError('OPENAI_API_KEY environment variable is required.')
    return OpenAI(api_key=api_key)
