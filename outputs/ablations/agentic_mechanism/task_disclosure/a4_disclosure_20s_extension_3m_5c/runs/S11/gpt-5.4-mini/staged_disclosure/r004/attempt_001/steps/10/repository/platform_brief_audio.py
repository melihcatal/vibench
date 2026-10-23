import base64
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import requests


@dataclass(frozen=True)
class AudioBriefConfig:
    api_key: str
    model: str = "gpt-4o-mini-tts"
    voice: str = "alloy"
    format: str = "mp3"
    base_url: str = "https://api.openai.com/v1"
    timeout: float = 60.0


def load_config(prefix: str = "AUDIO_BRIEF_") -> AudioBriefConfig:
    api_key = os.getenv(f"{prefix}API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing API key: set AUDIO_BRIEF_API_KEY or OPENAI_API_KEY")
    return AudioBriefConfig(
        api_key=api_key,
        model=os.getenv(f"{prefix}MODEL", "gpt-4o-mini-tts"),
        voice=os.getenv(f"{prefix}VOICE", "alloy"),
        format=os.getenv(f"{prefix}FORMAT", "mp3"),
        base_url=os.getenv(f"{prefix}BASE_URL", "https://api.openai.com/v1").rstrip("/"),
        timeout=float(os.getenv(f"{prefix}TIMEOUT", "60")),
    )


class OpenAITTSClient:
    def __init__(self, config: Optional[AudioBriefConfig] = None) -> None:
        self.config = config or load_config()
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            }
        )

    def _brief_text(self, platform_output: str) -> str:
        return f"Platform briefing: {platform_output.strip()}"

    def synthesize(self, platform_output: str) -> bytes:
        payload = {
            "model": self.config.model,
            "voice": self.config.voice,
            "input": self._brief_text(platform_output),
            "response_format": self.config.format,
        }
        response = self._session.post(
            f"{self.config.base_url}/audio/speech",
            json=payload,
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        return response.content

    def synthesize_to_file(self, platform_output: str, output_path: str) -> str:
        data = self.synthesize(platform_output)
        path = Path(output_path)
        path.write_bytes(data)
        return str(path)

    def synthesize_base64(self, platform_output: str) -> str:
        return base64.b64encode(self.synthesize(platform_output)).decode("ascii")


def generate_spoken_briefing(platform_output: str, output_path: Optional[str] = None) -> str:
    client = OpenAITTSClient()
    if output_path:
        return client.synthesize_to_file(platform_output, output_path)
    return client.synthesize_base64(platform_output)


def main() -> None:
    platform_output = os.getenv("PLATFORM_OUTPUT", "No platform output provided.")
    output_path = os.getenv("AUDIO_BRIEF_OUTPUT_PATH")
    result = generate_spoken_briefing(platform_output, output_path=output_path)
    print(result)


if __name__ == "__main__":
    main()
