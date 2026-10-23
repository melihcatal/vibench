from typing import Dict, Any
from translation_client import TranslationClient
from translation_models import parse_dictionary_translation_response
import json

def translate_dictionary_values(input_dict: Dict[str, Any], target_language: str, source_language: str = "en") -> Dict[str, str]:
    """
    Translates dictionary values while preserving keys using OpenAI.
    """
    client_manager = TranslationClient()
    client = client_manager.get_client()
    model_name = client_manager.get_model_name()

    # Prepare the dictionary for translation
    # We'll send it as a JSON string to the LLM and ask it to translate values
    dict_as_string = json.dumps(input_dict)

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": f"You are a helpful assistant that translates the VALUES within a JSON dictionary from {source_language} to {target_language}. You must preserve all dictionary keys exactly as they are. Return only the translated JSON dictionary. Do not include any other text or explanations."},
            {"role": "user", "content": f"Translate the values in the following JSON dictionary from {source_language} to {target_language}:\n\n{dict_as_string}"}
        ],
        temperature=0.7,
        max_tokens=2000,
        response_format={ "type": "json_object" }
    )

    translated_content = response.choices[0].message.content
    return parse_dictionary_translation_response(translated_content)
