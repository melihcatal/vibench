from google.cloud import texttospeech

def embed_script(script):
    client = texttospeech.TextToSpeechClient()
    response = client.analyze_prosody(request={
        'audio': texttospeech.SynthesizeSpeechRequest(input=texttospeech.SynthesisInput(text=script),
            voice=texttospeech.VoiceSelectionParams(language_code='en-US'),
            audio_config=texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)),
        'features': [texttospeech.ProsodyAnalysisFeatures.PITCH]
    })
    return response.pitch_contour
