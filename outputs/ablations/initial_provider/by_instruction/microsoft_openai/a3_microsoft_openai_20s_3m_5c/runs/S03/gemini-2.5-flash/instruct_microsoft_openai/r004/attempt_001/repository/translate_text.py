from translation_client import TranslationClient
from translation_models import normalize_text_input, parse_translation_response

def translate_text(text: str, target_language: str, source_language: str = "en") -> str:
    """
    Translates a single text string between languages using OpenAI.
    """
    client_manager = TranslationClient()
    client = client_manager.get_client()
    model_name = client_manager.get_model_name()

    normalized_text = normalize_text_input(text)

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": f"You are a helpful assistant that translates {source_language} to {target_language}."},
            {"role": "user", "content": f"Translate the following text from {source_language} to {target_language}:\n\n{normalized_text}"}
        ],
        temperature=0.7,
        max_tokens=1500
    )
    return parse_translation_response(response.choices[0].message.content)
