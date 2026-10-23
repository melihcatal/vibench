from google import genai
from google.genai import types
from model_client import get_platform_client, get_platform_model_id
from model_models import normalize_platform_text


def platform_brief_audio(text, voice_name="Kore"):
    client = get_platform_client()
    model_id = get_platform_model_id()
    prompt = f"Create a short spoken briefing from this text: {normalize_platform_text(text)}"
    response = client.models.generate_content(
        model=model_id,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice_name))),
        ),
    )
    return response