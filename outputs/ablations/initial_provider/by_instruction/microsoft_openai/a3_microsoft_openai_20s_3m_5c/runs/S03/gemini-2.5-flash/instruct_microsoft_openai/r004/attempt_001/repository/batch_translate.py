from typing import List
from translation_client import TranslationClient
from translation_models import normalize_batch_input, parse_translation_response

def batch_translate(texts: List[str], target_language: str, source_language: str = "en") -> List[str]:
    """
    Translates a list of strings while preserving order using OpenAI.
    """
    client_manager = TranslationClient()
    client = client_manager.get_client()
    model_name = client_manager.get_model_name()

    normalized_texts = normalize_batch_input(texts)
    combined_text = "\n--ITEM_SEPARATOR--\n".join(normalized_texts)

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": f"You are a helpful assistant that translates {source_language} to {target_language}. Translate the provided text, preserving the order of items separated by '--ITEM_SEPARATOR--'. Do not translate '--ITEM_SEPARATOR--'."},
            {"role": "user", "content": f"Translate the following list of texts from {source_language} to {target_language}:\n\n{combined_text}"}
        ],
        temperature=0.7,
        max_tokens=2000
    )
    translated_combined_text = parse_translation_response(response.choices[0].message.content)
    return [item.strip() for item in translated_combined_text.split("--ITEM_SEPARATOR--") if item.strip()]
