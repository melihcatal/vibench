from google.cloud import texttospeech

def embed_batch(texts):
    client = texttospeech.TextToSpeechClient()
    embeddings = []
    for text in texts:
        input_text = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
        embeddings.append(response.audio_content)
    return embeddings