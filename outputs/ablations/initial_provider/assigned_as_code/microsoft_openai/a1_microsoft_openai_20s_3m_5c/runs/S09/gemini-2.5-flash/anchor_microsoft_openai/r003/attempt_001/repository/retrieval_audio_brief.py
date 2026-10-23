import os
from google.cloud import texttospeech_v1 as texttospeech

def retrieval_audio_brief(payload: dict, config: dict = None) -> dict:
    config = config or {}
    
    # The Text-to-Speech client automatically handles project ID from environment variables or gcloud config
    client = texttospeech.TextToSpeechClient()

    brief_text = payload.get("brief_text", "")
    output_audio_file = payload.get("output_audio_file", "output.mp3")
    language_code = payload.get("language_code", "en-US")
    voice_name = payload.get("voice_name", "en-US-Standard-C")
    audio_encoding = payload.get("audio_encoding", "MP3")

    if not brief_text:
        return {"audio_brief_status": "No text provided for audio brief.", "output_file": output_audio_file}

    synthesis_input = texttospeech.SynthesisInput(text=brief_text)

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=getattr(texttospeech.AudioEncoding, audio_encoding.upper())
    )

    # Select the language and voice
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # The response's audio_content is binary. Need to save it to a file.
    # In a real scenario, this would likely be saved to a cloud storage bucket or returned as a base64 encoded string.
    with open(output_audio_file, "wb") as out:
        out.write(response.audio_content)

    return {"audio_brief_status": "Successfully generated audio brief.", "output_file": output_audio_file}
