from translation_client import get_openai_client
from translation_models import TranslationRequest, TranslationResponse
from typing import Dict, Any

def translate_dictionary_values(data: Dict[str, Any], target_language: str, source_language: str = "auto") -> Dict[str, Any]:
    client = get_openai_client()
    translated_data = {}

    for key, value in data.items():
        if isinstance(value, str):
            messages = [
                {"role": "system", "content": "You are a helpful translation assistant."},
                {"role": "user", "content": f"Translate the following text from {source_language} to {target_language}:\n\n{value}"}
            ]
            try:
                completion = client.chat.completions.create(
                    model="gpt-4o-mini",  # Using a concrete OpenAI model
                    messages=messages
                )
                translated_text = completion.choices[0].message.content.strip()
                translated_data[key] = translated_text
            except Exception as e:
                translated_data[key] = f"Error: {str(e)}"
        else:
            translated_data[key] = value
            
    return translated_data
