import azure.cognitiveservices.speech as speechsdk

def save_audio(audio_bytes, file_path):
    with open(file_path, 'wb') as f:
        f.write(audio_bytes)