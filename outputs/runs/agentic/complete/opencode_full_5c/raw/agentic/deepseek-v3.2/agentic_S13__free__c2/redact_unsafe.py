import os
import re
from openai import OpenAI
from typing import List, Tuple, Dict, Any


def redact_unsafe(text: str) -> Dict[str, Any]:
    """
    Flags or redacts unsafe spans from text using OpenAI's moderation API.
    Returns both the redacted text and the unsafe spans detected.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # First, moderate the text to get categories
    moderation_response = client.moderations.create(
        model="text-moderation-latest", input=text
    )

    result = moderation_response.results[0]

    # Use GPT-4 to identify and redact unsafe spans
    prompt = f"""Analyze the following text and identify specific spans that contain unsafe content.
    For each unsafe span, provide the exact text and the category of violation.
    Text: {text}
    
    Return a JSON with:
    1. "redacted_text": the original text with unsafe spans replaced with "[REDACTED]"
    2. "unsafe_spans": list of objects with "text", "start_index", "end_index", "category"
    """

    completion_response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a content safety analyzer. Identify unsafe spans in text.",
            },
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
    )

    analysis = eval(completion_response.choices[0].message.content)

    # Apply redactions
    redacted_text = text
    unsafe_spans = []

    if "unsafe_spans" in analysis:
        # Sort spans by start index in reverse to avoid index shifting issues
        spans = sorted(
            analysis["unsafe_spans"], key=lambda x: x["start_index"], reverse=True
        )

        for span in spans:
            start = span["start_index"]
            end = span["end_index"]
            original_span = text[start:end]

            # Replace with redaction marker
            redacted_text = redacted_text[:start] + "[REDACTED]" + redacted_text[end:]

            unsafe_spans.append(
                {
                    "text": original_span,
                    "start_index": start,
                    "end_index": end,
                    "category": span["category"],
                }
            )

    return {
        "redacted_text": redacted_text,
        "unsafe_spans": unsafe_spans,
        "moderation_result": {
            "flagged": result.flagged,
            "categories": {
                "hate": result.categories.hate,
                "hate/threatening": result.categories.hate_threatening,
                "harassment": result.categories.harassment,
                "harassment/threatening": result.categories.harassment_threatening,
                "self-harm": result.categories.self_harm,
                "self-harm/intent": result.categories.self_harm_intent,
                "self-harm/instructions": result.categories.self_harm_instructions,
                "sexual": result.categories.sexual,
                "sexual/minors": result.categories.sexual_minors,
                "violence": result.categories.violence,
                "violence/graphic": result.categories.violence_graphic,
            },
        },
    }
