import os
from google.cloud import genai, translate_v2 as translate

# Load Gemini model (Gemini Pro) from Vertex AI
# Ensure GOOGLE_APPLICATION_CREDENTIALS points to your credentials
# The model name matches the hosted LLM "hosted LLM Inference and Model-Family Selection" reference

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
client = genai.Service.from_pretrained('gemini-pro')

translate_client = translate.Client()

def summarize_asset(text: str, target_language: str = 'en') -> str:
    """
    Summarize text extracted from an asset using Gemini and optionally translate to target language.
    Returns a concise summary as a string.
    """
    # Sent to Gemini for summarization
    response = client.generate_content(
        prompt=f"Summarize the following text in {target_language}:\n\n{text}"
    )
    summary = response.text
    return summary
