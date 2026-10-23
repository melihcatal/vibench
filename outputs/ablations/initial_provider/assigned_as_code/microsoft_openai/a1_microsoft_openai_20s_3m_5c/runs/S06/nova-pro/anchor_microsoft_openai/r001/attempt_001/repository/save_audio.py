import azure.cognitiveservices.speech as speechsdk

def save_audio(audio_content, file_path):
    with open(file_path, 'wb') as outfile:
        outfile.write(audio_content)
