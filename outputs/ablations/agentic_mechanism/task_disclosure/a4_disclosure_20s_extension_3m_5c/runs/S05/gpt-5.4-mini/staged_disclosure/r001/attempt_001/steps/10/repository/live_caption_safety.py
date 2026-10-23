import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


class LiveCaptionSafetyChecker:
    def __init__(self, api_key: Optional[str] = None, model: str = OPENAI_MODEL) -> None:
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required")

    def check(self, transcript_text: str) -> Dict[str, Any]:
        prompt = (
            "Analyze this live transcript for unsafe content. "
            "Return strict JSON with keys: unsafe (boolean), categories (array of strings), "
            "severity (string), rationale (string), and should_interrupt (boolean).\n\n"
            f"Transcript:\n{transcript_text}"
        )
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a safety classifier for live captions."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        }
        response = requests.post(
            OPENAI_API_URL,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            data=json.dumps(payload),
            timeout=30,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return json.loads(content)


def check_live_transcript(transcript_text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    return LiveCaptionSafetyChecker(api_key=api_key).check(transcript_text)
