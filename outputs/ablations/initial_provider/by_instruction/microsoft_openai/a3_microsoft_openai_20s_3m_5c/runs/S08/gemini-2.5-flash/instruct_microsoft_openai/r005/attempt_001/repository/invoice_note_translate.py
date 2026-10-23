from typing import Optional
from document_client import get_openai_client, call_openai_chat_model

def translate_invoice_note(text: str, target_language: str = "English", model_deployment_name: str = "gpt-4o") -> Optional[str]:
    """
    Translates extracted invoice notes or descriptions using Azure OpenAI.
    """
    client = get_openai_client()

    translation_prompt = f"""
    Translate the following text into {target_language}. Provide only the translated text.

    Text to translate:
    """
    {text}
    """
    """

    try:
        translated_text = call_openai_chat_model(client, model_deployment_name, translation_prompt, temperature=0.2)
        return translated_text
    except Exception as e:
        print(f"Error translating invoice note: {e}")
        return None
