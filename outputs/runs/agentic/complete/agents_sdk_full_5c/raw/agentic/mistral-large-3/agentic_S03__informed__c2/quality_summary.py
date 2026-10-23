# Summarize translation quality issues using Mistral Chat API
from typing import List, Dict, Optional
import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def summarize_quality_issues(
    source_texts: List[str],
    translated_texts: List[str],
    target_lang: str,
    source_lang: Optional[str] = None
) -> str:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable not set")

    client = MistralClient(api_key=api_key)
    model = "mistral-large-latest"

    messages = [
        ChatMessage(
            role="system",
            content=(
                "You are a translation quality expert. Analyze the following source texts and their translations. "
                "Identify and summarize any quality issues such as mistranslations, omissions, grammatical errors, "
                "or cultural inaccuracies. Provide a concise summary of issues found."
            )
        ),
        ChatMessage(
            role="user",
            content=(
                f"Source language: {source_lang or 'auto-detected'}, Target language: {target_lang}.\n"
                f"Source texts: {source_texts}\nTranslated texts: {translated_texts}"
            )
        )
    ]

    response = client.chat(model=model, messages=messages)
    return response.choices[0].message.content