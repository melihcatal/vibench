import os
import logging
from typing import Optional, Dict, List, Any, Tuple

import openai

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

openai.api_key = OPENAI_API_KEY

ONBOARDING_COPY_TEMPLATES: Dict[str, List[str]] = {
    "welcome_message": [
        "Welcome to our platform! We're excited to have you on board.",
        "Your account has been successfully created. Let's get started.",
        "Hello and welcome! Explore your personalized dashboard now.",
    ],
    "next_steps": [
        "Complete your profile to personalize your experience.",
        "Connect with other users and join communities.",
        "Check out our getting started guide for tips.",
    ],
    "support_info": [
        "Need help? Contact our support team anytime.",
        "Visit our help center for FAQs and tutorials.",
        "Reach out to us via email or live chat for assistance.",
    ],
}


def translate_onboarding_copy(
    target_locale: str,
    copy_keys: Optional[List[str]] = None,
    model: Optional[str] = None,
) -> Tuple[Optional[Dict[str, Dict[str, str]]], Optional[str]]:
    target_model = model or OPENAI_MODEL
    keys_to_translate = copy_keys or list(ONBOARDING_COPY_TEMPLATES.keys())

    texts_to_translate: List[str] = []
    key_map: List[tuple] = []

    for key in keys_to_translate:
        if key in ONBOARDING_COPY_TEMPLATES:
            for idx, text in enumerate(ONBOARDING_COPY_TEMPLATES[key]):
                texts_to_translate.append(text)
                key_map.append((key, idx))

    if not texts_to_translate:
        return {}, None

    formatted_texts = "\n".join(
        f"[{i}] {text}" for i, text in enumerate(texts_to_translate)
    )

    system_prompt = (
        f"You are a professional translator. Translate the following English text "
        f"into {target_locale}. Preserve the numbering. Return only the translations, "
        f"one per line, matching the original numbering."
    )

    try:
        response = openai.chat.completions.create(
            model=target_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": formatted_texts},
            ],
            temperature=0.3,
        )

        translated_text = response.choices[0].message.content.strip()
        translated_lines = translated_text.split("\n")

        result: Dict[str, Dict[str, str]] = {}
        for (key, idx), translated_line in zip(key_map, translated_lines):
            if key not in result:
                result[key] = {}
            result[key][str(idx)] = translated_line.strip()

        logger.info(
            "Translated onboarding copy to %s using OpenAI %s",
            target_locale,
            target_model,
        )
        return result, None

    except openai.OpenAIError as exc:
        logger.error("OpenAI translation failed: %s", exc)
        return None, str(exc)
