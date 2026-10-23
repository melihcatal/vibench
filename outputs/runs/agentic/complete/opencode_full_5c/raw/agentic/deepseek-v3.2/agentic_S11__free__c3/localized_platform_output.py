import os
from typing import Dict, Any
from openai import OpenAI
from model_client import get_openai_client
from model_models import ChatResponse


def localized_platform_output(
    content: str, target_locale: str = "es"
) -> Dict[str, Any]:
    """
    Translate OpenAI model output for another locale using OpenAI's translation capabilities.
    """
    client = get_openai_client()

    # Map locale codes to language names
    locale_map = {
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "ja": "Japanese",
        "zh": "Chinese",
        "ko": "Korean",
        "ru": "Russian",
        "ar": "Arabic",
    }

    target_language = locale_map.get(target_locale, "Spanish")

    try:
        # Use OpenAI to translate the content
        translation_prompt = f"""
        Translate the following text to {target_language}. 
        Preserve the meaning, tone, and formatting as much as possible.
        
        Text to translate:
        {content}
        
        Translation:
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a professional translator specializing in {target_language}.",
                },
                {"role": "user", "content": translation_prompt},
            ],
            temperature=0.3,
            max_tokens=2000,
        )

        translated_content = response.choices[0].message.content

        # Get metadata about the translation
        translation_metadata = {
            "provider": "openai",
            "source_locale": "en",
            "target_locale": target_locale,
            "target_language": target_language,
            "translation_model": "gpt-4o",
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
        }

        return {
            "original_content": content,
            "translated_content": translated_content,
            "metadata": translation_metadata,
            "raw_openai_response": response,
        }

    except Exception as e:
        raise Exception(
            f"Failed to translate content to {target_locale} using OpenAI: {str(e)}"
        )
