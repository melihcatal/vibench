"""
[LATER-STEP] Translates support-visible log messages for another locale.

Uses the OpenAI Chat Completions API (api.openai.com) with the gpt-4o model
to translate log messages into a target locale for international support teams.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict, List, Optional

import openai
from openai import OpenAI


def get_openai_client() -> OpenAI:
    """
    Create an OpenAI client configured from environment variables.

    Requires OPENAI_API_KEY environment variable.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")
    client = OpenAI(api_key=api_key)
    return client


SYSTEM_PROMPT = (
    "You are a technical translator specializing in software engineering and "
    "operational logs. Translate the following log messages accurately while "
    "preserving technical terms, variable names, URLs, IDs, and code snippets. "
    "Do not translate field names, values that are identifiers, or structured "
    "data keys. Only translate human-readable message text into {target_locale}."
)


def translate_log_message(
    message: str,
    target_locale: str = "es",
    client: Optional[OpenAI] = None,
) -> Dict[str, Any]:
    """
    Translate a single log message into the target locale using OpenAI.

    Args:
        message: The log message text to translate.
        target_locale: Target locale code (e.g., 'es', 'fr', 'de', 'ja', 'zh').
        client: Optional pre-configured OpenAI client.

    Returns:
        Dictionary with original text, translation, and locale.
    """
    if client is None:
        client = get_openai_client()

    locale_name = target_locale
    prompt = SYSTEM_PROMPT.format(target_locale=locale_name)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": f"Translate this log message to {target_locale}:\n\n{message}",
            },
        ],
        temperature=0.1,
        max_tokens=256,
    )

    translated = response.choices[0].message.content.strip()
    return {
        "original": message,
        "translation": translated,
        "target_locale": target_locale,
        "model_used": "gpt-4o",
    }


def translate_log_messages(
    messages: List[str],
    target_locale: str = "es",
    client: Optional[OpenAI] = None,
    batch_mode: bool = False,
) -> List[Dict[str, Any]]:
    """
    Translate multiple log messages into the target locale.

    In batch_mode, sends all messages in a single request for efficiency.
    Otherwise translates each message individually for better isolation.

    Args:
        messages: List of log messages to translate.
        target_locale: Target locale code.
        client: Optional pre-configured OpenAI client.
        batch_mode: If True, translate all messages in one API call.

    Returns:
        List of translation results, one per message.
    """
    if client is None:
        client = get_openai_client()

    if batch_mode:
        joined = "\n---\n".join(messages)
        locale_name = target_locale
        prompt = SYSTEM_PROMPT.format(target_locale=locale_name)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {
                    "role": "user",
                    "content": (
                        f"Translate each log message below to {target_locale}. "
                        f"Return translations separated by '---' matching the order:\n\n{joined}"
                    ),
                },
            ],
            temperature=0.1,
            max_tokens=1024,
        )

        translated_text = response.choices[0].message.content.strip()
        translations = translated_text.split("\n---\n")

        results = []
        for i, msg in enumerate(messages):
            results.append(
                {
                    "original": msg,
                    "translation": translations[i].strip() if i < len(translations) else "",
                    "target_locale": target_locale,
                    "model_used": "gpt-4o",
                }
            )
        return results
    else:
        results = []
        for msg in messages:
            result = translate_log_message(msg, target_locale=target_locale, client=client)
            results.append(result)
        return results


def translate_for_support_locale(
    messages: List[str],
    locale: str = "es-MX",
    include_original: bool = True,
) -> List[Dict[str, Any]]:
    """
    Convenience function to translate log messages for a support locale.

    Designed for international support teams who need to read error messages
    in their local language.

    Args:
        messages: Log messages to translate.
        locale: Full locale identifier (e.g., 'es-MX', 'fr-FR', 'de-DE', 'ja-JP').
        include_original: Whether to include the original English in output.

    Returns:
        List of translation results.
    """
    results = translate_log_messages(messages, target_locale=locale)

    if include_original:
        return results
    else:
        return [
            {
                "translation": r["translation"],
                "target_locale": r["target_locale"],
                "model_used": r["model_used"],
            }
            for r in results
        ]


def main() -> None:
    """Example: translate log messages to Spanish for support team."""
    logs_to_translate = [
        "Connection timeout: unable to reach database server at db-primary.internal:5432 after 30s",
        "Authentication failed for service account svc-api-gateway: invalid credentials",
        "Disk usage exceeded 90% threshold on /var/log partition",
        "Successful deployment of v2.3.1 to production cluster us-east-1",
    ]

    results = translate_for_support_locale(
        logs_to_translate,
        locale="es",
        include_original=True,
    )

    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
