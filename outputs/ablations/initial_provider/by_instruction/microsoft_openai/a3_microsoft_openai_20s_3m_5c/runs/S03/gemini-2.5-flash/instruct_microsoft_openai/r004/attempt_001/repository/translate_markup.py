from translation_client import TranslationClient
from translation_models import normalize_text_input, parse_translation_response

def translate_markup(markup_text: str, target_language: str, source_language: str = "en") -> str:
    """
    Translates HTML or markup while preserving tags using OpenAI.
    """
    client_manager = TranslationClient()
    client = client_manager.get_client()
    model_name = client_manager.get_model_name()

    normalized_markup = normalize_text_input(markup_text)

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": f"You are a helpful assistant that translates {source_language} to {target_language}. Translate the content within HTML/XML tags, but strictly preserve all HTML/XML tags, attributes, and their structure. Do not add, remove, or modify any tags or attributes."},
            {"role": "user", "content": f"Translate the following markup from {source_language} to {target_language}:\n\n{normalized_markup}"}
        ],
        temperature=0.7,
        max_tokens=2000
    )
    return parse_translation_response(response.choices[0].message.content)
