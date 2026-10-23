import os
from typing import Dict, Any
from openai import OpenAI


def localized_platform_output(
    text: str, target_locale: str, model: str = "gpt-4o"
) -> Dict[str, Any]:
    """
    Translate platform model output for another locale using OpenAI's translation capabilities.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    # Map locale codes to language names for better prompting
    locale_map = {
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "it": "Italian",
        "pt": "Portuguese",
        "ja": "Japanese",
        "ko": "Korean",
        "zh": "Chinese",
        "ru": "Russian",
        "ar": "Arabic",
    }

    target_language = locale_map.get(target_locale, target_locale)

    # Create translation prompt
    translation_prompt = f"""Translate the following text to {target_language}. 
    Preserve the meaning, tone, and formatting as much as possible.
    
    Text to translate:
    {text}
    
    Translation:"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a professional translator."},
            {"role": "user", "content": translation_prompt},
        ],
        max_tokens=2000,
        temperature=0.3,
    )

    translated_text = response.choices[0].message.content

    # Get translation confidence by asking the model to evaluate its own translation
    evaluation_prompt = f"""Evaluate the quality of this translation from the original text to {target_language}.
    
    Original text: {text}
    Translated text: {translated_text}
    
    Provide a confidence score from 0-100 and brief explanation of any potential issues."""

    evaluation_response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a translation quality evaluator."},
            {"role": "user", "content": evaluation_prompt},
        ],
        max_tokens=500,
        temperature=0.2,
    )

    evaluation = evaluation_response.choices[0].message.content

    result = {
        "original_text": text,
        "translated_text": translated_text,
        "target_locale": target_locale,
        "target_language": target_language,
        "translation_model": model,
        "translation_usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        },
        "evaluation": evaluation,
        "evaluation_usage": {
            "prompt_tokens": evaluation_response.usage.prompt_tokens,
            "completion_tokens": evaluation_response.usage.completion_tokens,
            "total_tokens": evaluation_response.usage.total_tokens,
        },
    }

    return result
