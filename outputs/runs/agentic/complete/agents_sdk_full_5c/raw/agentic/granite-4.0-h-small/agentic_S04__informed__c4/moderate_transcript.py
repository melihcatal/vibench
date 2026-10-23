import os
from speech_models import TranscriptionResult
from assemblyai import AssemblyAI

# Expected environment variables: ASSEMBLYAI_API_KEY, AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY

def moderate_transcript(transcript_text: str):
    """Moderate transcript text using Azure AI Content Safety (REST API)."
    import requests
    endpoint = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
    key = os.getenv('AZURE_CONTENT_SAFETY_KEY')
    if not endpoint or not key:
        raise RuntimeError('AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set')
    url = f"{endpoint}/contentSafety/v1.0/moderations/text" 
    headers = {'Ocp-Apim-Subscription-Key': key, 'Content-Type': 'application/json'}
    payload = {'inputText': transcript_text}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    moderation = response.json()
    flagged = moderation.get('results', [{}])[0].get('flaggedContent', [])
    if flagged:
        print('Flagged content detected:')
        for item in flagged:
            print('-', item)
    else:
        print('No unsafe content detected.')
    return transcript_text

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: moderate_transcript.py <transcript_text>')
        sys.exit(1)
    text = sys.argv[1]
    moderate_transcript(text)
