import os
from google.cloud import texttospeech
from safety_models import ReviewerBriefAudioRequest, ReviewerBriefAudioResponse


def reviewer_brief_audio(payload: ReviewerBriefAudioRequest, config=None) -> ReviewerBriefAudioResponse:
    config = config or {}
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=payload.summary)

    voice = texttospeech.VoiceSelectionParams(
        language_code=payload.language_code,
        name=payload.voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response audio_content is binary. We should return it as a base64 encoded string if needed for transport,
    # but for simplicity, we'll return the raw bytes for now assuming the caller handles it.
    # In a real scenario, you might want to base64 encode this.
    return ReviewerBriefAudioResponse(audio_content=response.audio_content.hex())
