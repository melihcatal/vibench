import os
import json
from typing import Dict, List, Any, Optional
from openai import OpenAI
from messaging_models import normalize_payload, extract_text_from_payload


def summarize_message_results(
    messages: List[Dict[str, Any]], summary_prompt: Optional[str] = None
) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    extracted_texts = []
    for msg in messages:
        payload = normalize_payload(msg.get("data", msg))
        text = extract_text_from_payload(payload)
        if text:
            extracted_texts.append(text)

    if not extracted_texts:
        return {
            "summary": "No processable message content found.",
            "message_count": len(messages),
            "provider": "openai-gpt-4o",
            "model": "gpt-4o",
        }

    combined_text = "\n---\n".join(extracted_texts)

    default_prompt = (
        "Summarize the following message processing results. "
        "Identify key events, patterns, and any notable outcomes. "
        "Keep the summary concise and structured."
    )
    system_prompt = summary_prompt or default_prompt

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": combined_text},
        ],
        max_tokens=500,
        temperature=0.3,
    )

    summary_text = response.choices[0].message.content
    usage = response.usage

    return {
        "summary": summary_text,
        "message_count": len(messages),
        "provider": "openai-gpt-4o",
        "model": "gpt-4o",
        "prompt_tokens": usage.prompt_tokens,
        "completion_tokens": usage.completion_tokens,
        "total_tokens": usage.total_tokens,
    }


def summarize_single_message(
    message_data: Dict[str, Any], summary_prompt: Optional[str] = None
) -> Dict[str, Any]:
    return summarize_message_results([message_data], summary_prompt)


if __name__ == "__main__":
    sample_messages = [
        {
            "data": {
                "user_id": "u1",
                "action": "login",
                "details": "User logged in from Chrome on macOS",
            }
        },
        {
            "data": {
                "user_id": "u2",
                "action": "purchase",
                "details": "Purchased item SKU-123 for $49.99",
            }
        },
        {
            "data": {
                "user_id": "u1",
                "action": "logout",
                "details": "Session ended after 15 minutes",
            }
        },
    ]
    result = summarize_message_results(sample_messages)
    print(json.dumps(result, indent=2))
