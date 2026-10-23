from safety_client import configure_client, load_config
from google.cloud import texttospeech

BRIEF_PROMPT_PREFIX = "Reviewer brief: "


def generate_reviewer_brief_audio(text: str) -> bytes:
    cfg = configure_client(load_config())
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=BRIEF_PROMPT_PREFIX + text)
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", name=cfg.tts_voice)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    return response.audio_content
