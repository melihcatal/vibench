import base64
import json
import mimetypes
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional
from urllib import error, request


OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_TRANSCRIPTION_MODEL = os.environ.get("OPENAI_TRANSCRIPTION_MODEL", "gpt-4o-mini-transcribe")


@dataclass(frozen=True)
class SpeechClientConfig:
    api_key: str
    transcription_model: str = OPENAI_TRANSCRIPTION_MODEL
    api_base: str = OPENAI_API_BASE
    timeout_seconds: int = 300


def load_config() -> SpeechClientConfig:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return SpeechClientConfig(
        api_key=api_key,
        transcription_model=os.environ.get("OPENAI_TRANSCRIPTION_MODEL", OPENAI_TRANSCRIPTION_MODEL),
        api_base=os.environ.get("OPENAI_API_BASE", OPENAI_API_BASE),
        timeout_seconds=int(os.environ.get("OPENAI_TIMEOUT_SECONDS", "300")),
    )


def build_audio_input(audio_path: str) -> Dict[str, str]:
    path = Path(audio_path)
    audio_bytes = path.read_bytes()
    mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return {
        "type": "input_audio",
        "audio": base64.b64encode(audio_bytes).decode("ascii"),
        "format": mime_type,
        "filename": path.name,
    }


def submit_batch_transcription(audio_path: str, config: Optional[SpeechClientConfig] = None) -> Dict[str, Any]:
    cfg = config or load_config()
    payload = {
        "model": cfg.transcription_model,
        "input": [build_audio_input(audio_path)],
    }
    req = request.Request(
        f"{cfg.api_base}/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {cfg.api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=cfg.timeout_seconds) as resp:
            return json.load(resp)
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API error {exc.code}: {body}") from exc


def extract_transcript(response: Dict[str, Any]) -> str:
    output = response.get("output", [])
    texts = []
    for item in output:
        content = item.get("content", []) if isinstance(item, dict) else []
        for part in content:
            if isinstance(part, dict) and part.get("type") in {"output_text", "text"}:
                text = part.get("text")
                if text:
                    texts.append(text)
    transcript = "\n".join(texts).strip()
    if transcript:
        return transcript
    if isinstance(response.get("text"), str):
        return response["text"]
    raise RuntimeError("No transcript text found in response")


def save_response(response: Dict[str, Any], output_path: str) -> None:
    Path(output_path).write_text(json.dumps(response, ensure_ascii=False, indent=2), encoding="utf-8")
