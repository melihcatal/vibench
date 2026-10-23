import os
from openai import OpenAI
from typing import Dict, Any


def appeal_translate(appeal_text: str, target_language: str = "en") -> Dict[str, Any]:
    """
    Translate appeal text for review using OpenAI's translation capabilities.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Use GPT-4 for translation with context about moderation appeals
    prompt = f"""Translate the following appeal text to {target_language}. 
    This is a content moderation appeal, so maintain the tone and intent accurately.
    
    Appeal text: {appeal_text}
    
    Return a JSON object with:
    - "original_text": the original appeal text
    - "translated_text": the translated text
    - "target_language": the target language code
    - "translation_confidence": your confidence in the translation (0.0 to 1.0)
    - "key_phrases": list of important phrases in the appeal
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a professional translator specializing in legal and moderation appeals.",
            },
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
    )

    translation_result = eval(response.choices[0].message.content)

    # Also moderate the translated text to check for safety issues
    moderation_response = client.moderations.create(
        model="text-moderation-latest", input=translation_result["translated_text"]
    )

    moderation_result = moderation_response.results[0]

    translation_result.update(
        {
            "moderation_check": {
                "flagged": moderation_result.flagged,
                "categories": {
                    "hate": moderation_result.categories.hate,
                    "hate/threatening": moderation_result.categories.hate_threatening,
                    "harassment": moderation_result.categories.harassment,
                    "harassment/threatening": moderation_result.categories.harassment_threatening,
                    "self-harm": moderation_result.categories.self_harm,
                    "self-harm/intent": moderation_result.categories.self_harm_intent,
                    "self-harm/instructions": moderation_result.categories.self_harm_instructions,
                    "sexual": moderation_result.categories.sexual,
                    "sexual/minors": moderation_result.categories.sexual_minors,
                    "violence": moderation_result.categories.violence,
                    "violence/graphic": moderation_result.categories.violence_graphic,
                },
            }
        }
    )

    return translation_result
