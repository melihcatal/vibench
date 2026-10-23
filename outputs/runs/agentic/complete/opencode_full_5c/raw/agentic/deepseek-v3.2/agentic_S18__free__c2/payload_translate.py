import os
from typing import Dict, Any
from google.cloud import translate_v2 as translate
import json


def translate_message_payload(
    payload: Dict[str, Any], target_language: str = "es"
) -> Dict[str, Any]:
    """Translate customer-facing message payload text using Google Cloud Translation API."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")

    client = translate.Client()

    translated_payload = payload.copy()

    text_fields_to_translate = extract_translatable_text(payload)

    for field_path, text in text_fields_to_translate.items():
        if text and isinstance(text, str) and text.strip():
            try:
                result = client.translate(
                    text, target_language=target_language, source_language="en"
                )

                set_nested_value(
                    translated_payload, field_path, result["translatedText"]
                )

            except Exception as e:
                print(f"Failed to translate field {field_path}: {e}")

    translated_payload["translation_metadata"] = {
        "target_language": target_language,
        "source_language": "en",
        "translated_at": "2024-01-15T10:30:00Z",
    }

    return translated_payload


def extract_translatable_text(data: Any, current_path: str = "") -> Dict[str, str]:
    """Extract text fields that should be translated from payload."""
    translatable_fields = {}

    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{current_path}.{key}" if current_path else key

            if key in ["message", "description", "title", "content", "body", "text"]:
                if isinstance(value, str):
                    translatable_fields[new_path] = value
                elif isinstance(value, dict):
                    translatable_fields.update(
                        extract_translatable_text(value, new_path)
                    )
                elif isinstance(value, list):
                    for i, item in enumerate(value):
                        list_path = f"{new_path}[{i}]"
                        if isinstance(item, str):
                            translatable_fields[list_path] = item
                        elif isinstance(item, dict):
                            translatable_fields.update(
                                extract_translatable_text(item, list_path)
                            )
            elif isinstance(value, dict):
                translatable_fields.update(extract_translatable_text(value, new_path))
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    list_path = f"{new_path}[{i}]"
                    if isinstance(item, dict):
                        translatable_fields.update(
                            extract_translatable_text(item, list_path)
                        )

    return translatable_fields


def set_nested_value(data: Dict[str, Any], path: str, value: Any) -> None:
    """Set value in nested dictionary using dot notation path."""
    parts = path.split(".")
    current = data

    for i, part in enumerate(parts[:-1]):
        if "[" in part and "]" in part:
            key = part[: part.index("[")]
            index = int(part[part.index("[") + 1 : part.index("]")])

            if key not in current:
                current[key] = []
            while len(current[key]) <= index:
                current[key].append({})

            current = current[key][index]
        else:
            if part not in current:
                current[part] = {}
            current = current[part]

    last_part = parts[-1]
    if "[" in last_part and "]" in last_part:
        key = last_part[: last_part.index("[")]
        index = int(last_part[last_part.index("[") + 1 : last_part.index("]")])

        if key not in current:
            current[key] = []
        while len(current[key]) <= index:
            current[key].append("")

        current[key][index] = value
    else:
        current[last_part] = value


if __name__ == "__main__":
    sample_payload = {
        "message": "Welcome to our service! Your account has been created successfully.",
        "user": {
            "name": "John Doe",
            "welcome_message": "Thank you for joining our platform.",
        },
        "instructions": [
            "Check your email for verification",
            "Complete your profile setup",
            "Explore available features",
        ],
    }

    try:
        translated = translate_message_payload(sample_payload, "fr")
        print("Translated Payload:")
        print(json.dumps(translated, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Failed to translate payload: {e}")
