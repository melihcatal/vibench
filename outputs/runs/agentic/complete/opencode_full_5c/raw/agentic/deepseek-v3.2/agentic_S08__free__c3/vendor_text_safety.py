import os
from openai import OpenAI
from document_client import load_config


def moderate_vendor_notes(vendor_name, notes_text):
    config = load_config()

    client = OpenAI(api_key=config["openai_api_key"])

    prompt = f"""Analyze this vendor note for safety and appropriateness:

Vendor: {vendor_name}
Notes: {notes_text}

Check for:
1. Hate speech, harassment, or discrimination
2. Violence or threats
3. Sexual content
4. Self-harm content
5. Hateful content
6. Harassment
7. Illegal activity

Return a JSON object with:
- "is_safe": boolean
- "categories": array of categories that triggered (empty if safe)
- "confidence": float between 0 and 1
- "reason": brief explanation
- "suggested_action": what to do if unsafe"""

    response = client.chat.completions.create(
        model=config["openai_model"],
        messages=[
            {
                "role": "system",
                "content": "You are a content moderation assistant. Analyze text for safety and return JSON.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=300,
        response_format={"type": "json_object"},
    )

    moderation_result = response.choices[0].message.content

    import json

    result = json.loads(moderation_result)

    result["vendor"] = vendor_name
    result["notes_preview"] = (
        notes_text[:100] + "..." if len(notes_text) > 100 else notes_text
    )
    result["moderation_model"] = config["openai_model"]

    return result
