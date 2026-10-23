import os
from typing import Dict, Any, List, Tuple
import openai
import re


def redact_unsafe(text: str) -> Dict[str, Any]:
    """
    Flags or redacts unsafe spans from text using OpenAI's moderation API with detailed analysis.
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    moderation_response = client.moderations.create(
        model="text-moderation-latest", input=text
    )

    result = moderation_response.results[0]

    redacted_text = text
    flagged_spans = []

    if result.flagged:
        chat_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a content safety analyzer. Identify specific unsafe spans in the text that violate content policies. Return only the unsafe phrases or words, one per line.",
                },
                {"role": "user", "content": f"Identify unsafe content in: {text}"},
            ],
            temperature=0.1,
            max_tokens=100,
        )

        unsafe_phrases = chat_response.choices[0].message.content.strip().split("\n")

        for phrase in unsafe_phrases:
            phrase = phrase.strip()
            if phrase and phrase in text:
                start_idx = text.find(phrase)
                end_idx = start_idx + len(phrase)
                flagged_spans.append(
                    {
                        "text": phrase,
                        "start": start_idx,
                        "end": end_idx,
                        "category": "unsafe_content",
                    }
                )
                redacted_text = redacted_text.replace(phrase, "[REDACTED]")

    return {
        "original_text": text,
        "redacted_text": redacted_text,
        "flagged": result.flagged,
        "flagged_spans": flagged_spans,
        "category_flags": {
            category: getattr(result.categories, category)
            for category in ["hate", "harassment", "sexual", "violence", "self_harm"]
        },
    }
