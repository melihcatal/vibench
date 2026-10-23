import json
import urllib.request

from speech_client import auth_headers, openai_base_url, load_speech_config


def translate_transcript(segments: list, target_language: str) -> str:
    cfg = load_speech_config()
    text = "\n".join(segment.get("text", "") for segment in segments)
    req = urllib.request.Request(
        f"{openai_base_url()}/responses",
        data=json.dumps(
            {
                "model": cfg.text_model,
                "input": f"Translate the following transcript into {target_language}:\n{text}",
            }
        ).encode("utf-8"),
        headers={**auth_headers(), "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8")).get("output_text", "")
