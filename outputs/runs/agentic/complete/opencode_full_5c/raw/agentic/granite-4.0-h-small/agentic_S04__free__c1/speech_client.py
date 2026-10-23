# speech_client.py
import os
import requests

# Provider: Azure Speech Service (provider identifiable via endpoint and key)
AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')
AZURE_ENDPOINT = os.getenv('AZURE_ENDPOINT')

def _build_headers():
    return {
        'Ocp-Apim-Subscription-Key': AZURE_SPEECH_KEY,
        'Content-Type': 'multipart/form-data'
    }

def _build_payload(audio_path):
    boundary = '---batch_boundary---'
    with open(audio_path, 'rb') as f:
        file_data = f.read()
    payload = (
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"file\"; filename=\"{os.path.basename(audio_path)}\"\r\n"
        f"Content-Type: audio/wav\r\n\r\n"
        f"{file_data.decode('latin-1')}\r\n"
        f"--{boundary}--\r\n"
    )
    return payload, boundary

def submit_transcription(audio_path):
    url = f"{AZURE_ENDPOINT}/speech/batch/v1.0/transcriptions"
    headers = _build_headers()
    payload, boundary = _build_payload(audio_path)
    response = requests.post(url, headers=headers, data=payload, headers={'Content-Type': f'multipart/form-data; boundary={boundary}'})
    response.raise_for_status()
    return response.json()
