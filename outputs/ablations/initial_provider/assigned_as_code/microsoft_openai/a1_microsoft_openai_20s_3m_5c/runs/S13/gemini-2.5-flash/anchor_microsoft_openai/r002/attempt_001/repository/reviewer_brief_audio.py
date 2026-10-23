from google.cloud import texttospeech

def reviewer_brief_audio(payload, config=None):
    config = config or {}
    client = texttospeech.TextToSpeechClient()

    text_to_synthesize = payload['brief_text']

    # Configure the synthesis request
    synthesis_input = texttospeech.SynthesisInput(text=text_to_synthesize)

    # Select the voice parameters
    voice = texttospeech.VoiceSelectionParams(
        language_code=config.get('language_code', 'en-US'),
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL # Or MALE/FEMALE
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    try:
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        # The response's audio_content is binary. In a real app, this would be saved to a file or streamed.
        # For this exercise, we'll return a placeholder or base64 encoded string (not actual base64 for simplicity).
        audio_content_base64 = "<base64_encoded_audio_content>" # In a real app, do base64.b64encode(response.audio_content).decode('utf-8')

    except Exception as e:
        audio_content_base64 = f"Error generating audio: {e}"

    return {'brief_text': text_to_synthesize, 'audio_content_base64': audio_content_base64}