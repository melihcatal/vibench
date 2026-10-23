import os
from pathlib import Path
from model_client import build_client, load_config, select_model_for_task
from model_models import SpeechBrief
from openai import OpenAI


def generate_spoken_brief(text: str, audio_path: str = "brief.mp3") -> SpeechBrief:
    config = load_config(select_model_for_task("answer"))
    client = build_client(config)
    resp = client.chat.completions.create(
        model=config.model,
        messages=[
            {"role": "system", "content": "Rewrite the content as a short spoken brief."},
            {"role": "user", "content": text},
        ],
        temperature=0.2,
    )
    brief = resp.choices[0].message.content
    tts = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    audio = tts.audio.speech.create(model="gpt-4o-mini-tts", voice="alloy", input=brief)
    Path(audio_path).write_bytes(audio.read())
    return SpeechBrief(text=brief, audio_path=audio_path)
