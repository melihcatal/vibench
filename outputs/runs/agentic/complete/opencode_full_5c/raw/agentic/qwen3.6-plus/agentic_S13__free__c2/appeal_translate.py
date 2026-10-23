from safety_client import get_openai_client, OPENAI_CHAT_MODEL
from safety_models import AppealTranslation


SUPPORTED_LANGUAGES = [
    "English",
    "Spanish",
    "French",
    "German",
    "Chinese",
    "Japanese",
    "Korean",
    "Arabic",
    "Portuguese",
    "Russian",
    "Hindi",
    "Italian",
    "Dutch",
    "Turkish",
    "Polish",
]


def translate_appeal(appeal_text, target_language="English"):
    if target_language not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"Unsupported target language: {target_language}. "
            f"Supported: {', '.join(SUPPORTED_LANGUAGES)}"
        )
    client = get_openai_client()
    system_prompt = (
        "You are a professional translator specializing in content moderation appeals. "
        "Translate the user's appeal text accurately while preserving the original tone, "
        "intent, and any policy-relevant details. First detect the source language, then "
        "provide the translation."
    )
    user_prompt = (
        f"Translate the following appeal text to {target_language}.\n\n"
        f"Appeal text: {appeal_text}\n\n"
        f"Respond in JSON format with keys: source_language, translated_text."
    )
    response = client.chat.completions.create(
        model=OPENAI_CHAT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
        max_tokens=512,
        response_format={"type": "json_object"},
    )
    import json

    result_text = response.choices[0].message.content.strip()
    parsed = json.loads(result_text)
    return AppealTranslation(
        original_text=appeal_text,
        target_language=target_language,
        translated_text=parsed.get("translated_text", ""),
        source_language_detected=parsed.get("source_language", "unknown"),
    )


def translate_appeal_batch(appeals, target_language="English"):
    results = []
    for appeal in appeals:
        results.append(translate_appeal(appeal, target_language))
    return results


def summarize_appeal(appeal_text):
    client = get_openai_client()
    system_prompt = (
        "You are a content moderation review assistant. Summarize user appeals concisely, "
        "highlighting the key arguments, any claimed misunderstandings, and the requested action."
    )
    response = client.chat.completions.create(
        model=OPENAI_CHAT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Summarize this appeal: {appeal_text}"},
        ],
        temperature=0.0,
        max_tokens=256,
    )
    return response.choices[0].message.content.strip()
