import os
import json
import requests

API_KEY = os.getenv("DEEPL_AUTH_KEY")
BASE_URL = "https://api.deepl.com/v2/translate"


def translate_text(text: str, target_lang: str = "EN") -> str:
    """Translate narration scripts using DeepL API (service=DeepL)."""
    if not API_KEY:
        raise RuntimeError(
            "Set DEEPL_AUTH_KEY environment variable for DeepL translation"
        )
    params = {"text": text, "target_lang": target_lang, "auth_key": API_KEY}
    resp = requests.post(BASE_URL, data=params)
    resp.raise_for_status()
    data = resp.json()
    translations = data.get("translations", [])
    if not translations:
        raise RuntimeError("Translation API returned no data")
    return translations[0]["text"]


class ScriptTranslate:
    """Higher‑level helper for translating entire script files or sections."""

    @staticmethod
    def translate_file(input_path: str, output_path: str, target_lang: str = "EN"):
        """Read JSON lines from input_path, translate each entry, write a new JSONL file."""
        with (
            open(input_path, "r", encoding="utf-8") as fin,
            open(output_path, "w", encoding="utf-8") as fout,
        ):
            for line in fin:
                entry = json.loads(line)
                entry["translated"] = translate_text(entry["text"], target_lang)
                fout.write(json.dumps(entry) + "\n")

    @staticmethod
    def translate_single(text: str, target_lang: str = "EN") -> dict:
        result = translate_text(text, target_lang)
        return {"text": result, "language": target_lang}
