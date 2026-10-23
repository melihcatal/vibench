from google.cloud import texttospeech
import os

def retrieval_audio_brief(payload, config=None):
    config = config or {}
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"
    client = texttospeech.TextToSpeechClient()

    brief_text = payload["brief_text"]
    output_file_path = payload.get("output_file_path", "audio_brief.mp3")

    synthesis_input = texttospeech.SynthesisInput(text=brief_text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_file_path, "wb") as out:
        out.write(response.audio_content)

    return {"status": "success", "output_file": output_file_path}
