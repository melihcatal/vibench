from __future__ import annotations

import base64

from model_client import choose_model, get_client


def spoken_brief(text: str, voice: str = "alloy", model: str | None = None) -> dict:
    selected_model = choose_model("spoken_brief", model)
    response = get_client().audio.speech.create(
        model=selected_model,
        voice=voice,
        input=text.strip(),
        format="mp3",
    )
    audio_bytes = response.read()
    return {
        "provider": "openai",
        "model": selected_model,
        "voice": voice,
        "audio_base64": base64.b64encode(audio_bytes).decode("ascii"),
    }
