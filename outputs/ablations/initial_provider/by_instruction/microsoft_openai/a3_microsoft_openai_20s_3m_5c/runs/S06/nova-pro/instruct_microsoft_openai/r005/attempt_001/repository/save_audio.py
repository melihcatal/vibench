from speech_client import SpeechClient

def save_audio(api_key, endpoint, audio_data, file_path):
    client = SpeechClient(api_key, endpoint)
    client.save_audio(audio_data, file_path)