from google.cloud import texttospeech
import os

def localized_audio_preview(payload):
    client = texttospeech.TextToSpeechClient()

    text_content = payload['text']
    language_code = payload['language_code']
    voice_gender = payload.get('voice_gender', 'NEUTRAL') # Default to NEUTRAL

    synthesis_input = texttospeech.SynthesisInput(text=text_content)

    voice_selection_params = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender[voice_gender]
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice_selection_params,
        audio_config=audio_config
    )

    # The response's audio_content is binary. It can be saved to a file or streamed.
    # For this task, we'll return the base64 encoded audio content.
    import base64
    return {"audio_content_mp3_base64": base64.b64encode(response.audio_content).decode('utf-8')}
