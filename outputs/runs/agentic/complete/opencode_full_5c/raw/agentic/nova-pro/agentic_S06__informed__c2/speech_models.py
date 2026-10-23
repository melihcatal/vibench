from azure.cognitiveservices.speech.audio import AudioDataStream


def normalize_response(response):
    return AudioDataStream(response.audio_data)
