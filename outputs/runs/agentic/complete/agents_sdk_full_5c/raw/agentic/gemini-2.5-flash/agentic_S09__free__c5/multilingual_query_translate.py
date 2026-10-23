import os
from google.cloud import aiplatform

# Initialize Vertex AI client for generative AI
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")
aiplatform.init(project=PROJECT_ID, location=LOCATION)

def translate_query(query: str, target_language: str = "en") -> str:
    """
    Translates a query into a target language using Google Cloud Vertex AI's `gemini-pro` model.
    This allows for multilingual search by translating queries before embedding.

    Args:
        query: The original query string.
        target_language: The ISO 639-1 code of the target language (e.g., "en", "es", "fr").

    Returns:
        The translated query string.
    """
    model = aiplatform.GenerativeModel("gemini-pro") # Concrete model identifier

    prompt = f"""Translate the following query into {target_language}.
If the query is already in {target_language}, return it as is.
Only provide the translated text and nothing else.

Query: "{query}"

Translation:
"""
    response = model.generate_content(prompt)
    return response.candidates[0].content.text.strip()

if __name__ == '__main__':
    spanish_query = "Hola, ¿cómo estás?"
    french_query = "Où est la bibliothèque?"
    english_query = "What is the capital of France?"

    translated_to_english_from_spanish = translate_query(spanish_query, "en")
    print(f"'{spanish_query}' translated to English: '{translated_to_english_from_spanish}'")

    translated_to_english_from_french = translate_query(french_query, "en")
    print(f"'{french_query}' translated to English: '{translated_to_english_from_french}'")

    translated_to_spanish_from_english = translate_query(english_query, "es")
    print(f"'{english_query}' translated to Spanish: '{translated_to_spanish_from_english}'")

    already_english = translate_query(english_query, "en")
    print(f"'{english_query}' (already English) translated to English: '{already_english}'")
