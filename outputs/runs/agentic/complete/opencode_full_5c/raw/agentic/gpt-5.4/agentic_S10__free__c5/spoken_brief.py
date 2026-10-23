from model_client import get_chat_model, get_openai_client, get_tts_model
from model_models import AudioResult, normalize_text


def generate_spoken_brief(text: str, voice: str = "alloy") -> AudioResult:
    client = get_openai_client()
    brief_response = client.responses.create(
        model=get_chat_model("spoken_brief", default_model="gpt-4.1-mini"),
        input=[
            {
                "role": "system",
                "content": "Rewrite the text as a concise spoken brief for audio narration.",
            },
            {"role": "user", "content": text},
        ],
        max_output_tokens=220,
        temperature=0.3,
    )
    transcript = normalize_text(brief_response.output_text)
    audio_response = client.audio.speech.create(
        model=get_tts_model(),
        voice=voice,
        input=transcript,
        format="mp3",
    )
    return AudioResult(
        provider="OpenAI",
        model=get_tts_model(),
        audio_bytes=audio_response.read(),
        transcript=transcript,
    )
