import os

from google.cloud import texttospeech_v1 as texttospeech


def retrieval_audio_brief(payload, config=None):
    config = config or {}
    client = texttospeech.TextToSpeechClient()

    text_content = payload["brief_text"]
    output_filepath = payload.get("output_filepath", "audio_brief.mp3")

    synthesis_input = texttospeech.SynthesisInput(text=text_content)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={
            "input": synthesis_input, "voice": voice, "audio_config": audio_config
        }
    )

    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)

    return {"message": f"Audio brief generated and saved to {output_filepath}", "output_filepath": output_filepath}
