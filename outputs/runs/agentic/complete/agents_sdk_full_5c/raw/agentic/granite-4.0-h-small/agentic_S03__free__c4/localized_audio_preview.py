import os
from typing import List
import requests
from translation_client import TranslationClient

def generate_spoken_previews(texts: List[str], language: str = 'es') -> List[str]:
    """Translate texts and then call a hypothetical Text-to-Speech (TTS) service to produce audio previews.
    Provider #1: Azure Cognitive Services Translator (identified by env var AZURE_TRANSLATOR_KEY).
    Provider #2: Azure TTS (identified by env var AZURE_SPEECH_KEY and AZURE_SPEECH_REGION).
    """
    translator = TranslationClient()
    endpoint = os.getenv('AZURE_SPEECH_ENDPOINT')
    key = os.getenv('AZURE_SPEECH_KEY')
    region = os.getenv('AZURE_SPEECH_REGION')
    if not all([endpoint, key, region]):
        raise RuntimeError('Missing Azure Speech environment variables')

    # Step 1: Translate each text to the target language
    translated = []
    for txt in texts:
        payload = [
            {'Text': txt, 'SourceLanguage': 'en', 'TargetLanguage': language}
        ]
        resp_json = translator._request('translate', payload)
        translated.append(json.loads(resp_json)[0]['translations'][0]['text'])

    # Step 2: Call TTS API for each translated string
    audio_urls = []
    tts_url = f'{endpoint}/cognitiveservices/v1?api-version=1.0'
    headers = {
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/ssml+xml',
        'X-Search-AppId': 'DummyAppId',
        'X-Search-ClientID': 'DummyClientId'
    }
    for txt in translated:
        ssml = f'<speak version="1.0"><voice name="en-US-JennyNeural">{txt}</voice></speak>'
        tts_resp = requests.post(tts_url, headers=headers, params={'voice': 'en-US-JennyNeural', 'output': 'audio-16khz-64kbitrate-mono-mp3'}, data=ssml.encode('utf-8'))
        tts_resp.raise_for_status()
        audio_urls.append(tts_resp.headers['Content-Location'])  # URL to the generated audio file
    return audio_urls

if __name__ == '__main__':
    demo = ['Hello world', 'Goodbye']
    print('Audio preview URLs:')
    for url in generate_spoken_previews(demo):
        print(url)