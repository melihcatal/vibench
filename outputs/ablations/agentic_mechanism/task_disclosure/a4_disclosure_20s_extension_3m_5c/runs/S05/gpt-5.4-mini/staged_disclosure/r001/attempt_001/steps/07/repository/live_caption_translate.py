import os
import sys
import json
import queue
import threading
from dataclasses import dataclass

from google.cloud import translate_v2 as translate


@dataclass
class CaptionEvent:
    text: str


class LiveCaptionTranslator:
    def __init__(self, target_language: str, project_id: str | None = None):
        self.target_language = target_language
        self.project_id = project_id
        self.client = translate.Client(project=project_id)

    def translate_text(self, text: str) -> str:
        if not text.strip():
            return text
        result = self.client.translate(text, target_language=self.target_language)
        translated = result.get("translatedText", "")
        return translated


def _iter_caption_events() -> CaptionEvent:
    for line in sys.stdin:
        text = line.rstrip("\n")
        if text:
            yield CaptionEvent(text=text)


def main() -> int:
    target_language = os.environ.get("TARGET_LANGUAGE", "es")
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    translator = LiveCaptionTranslator(target_language=target_language, project_id=project_id)
    for event in _iter_caption_events():
        translated = translator.translate_text(event.text)
        sys.stdout.write(json.dumps({"source": event.text, "translated": translated}, ensure_ascii=False) + "\n")
        sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
