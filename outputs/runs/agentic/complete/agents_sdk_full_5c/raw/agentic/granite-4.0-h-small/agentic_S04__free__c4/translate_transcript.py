import os
import json
from speech_client import SpeechClient
from speech_models import TranscriptionResult

# Provider-specific: Azure Cognitive Services Translator
AZURE_TRANSLATOR_ENDPOINT = os.getenv('AZURE_TRANSLATOR_ENDPOINT')
AZURE_TRANSLATOR_KEY = os.getenv('AZURE_TRANSLATOR_KEY')

translator = SpeechClient(
    base_url=AZURE_TRANSLATOR_ENDPOINT,
    api_key=AZURE_TRANSLATOR_KEY,
    provider='azure_translator'
)

def translate_transcript(job_id: str, target_lang: str = 'es', source_lang: str = 'en-US') -> Dict:
    """Translate the completed transcript of a batch job.

    Args:
        job_id (str): Batch transcription job identifier.
        target_lang (str): ISO-639-1 code of the target language.
        source_lang (str): ISO-639-1 code of the source language (defaults to en-US).
    Returns:
        dict: JSON payload containing translated text segments.
    """
    # Assume the transcription result is already retrieved via poll_transcription
    transcript = poll_transcription(job_id)  # type: ignore
    audio_url = transcript.get('outputUrl')

    payload = {
        'inputs': [
            {
                'text': '[PLACEHOLDER]',  # will be replaced by real transcript text per segment
                'sourceLanguage': source_lang,
                'targetLanguage': target_lang
            }
        ]
    }

    response = translator.post('/translate', json=payload, params={'api-version': '3.0'})
    return response.json()

# Helper that calls poll_transcription internally
if __name__ == '__main__':
    # Example usage (replace with real job ID)
    job_id = 'abc123-0000-1111-2222'
    translation = translate_transcript(job_id, target_lang='es')
    print('Translated transcript:', translation)
