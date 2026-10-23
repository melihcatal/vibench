import json
from speech_client import SpeechClient
from speech_models import TranscriptionResult

# Provider-specific: Azure Storage Blob for archiving summaries
STORAGE_ACCOUNT = os.getenv('AZURE_STORAGE_ACCOUNT')
STORAGE_CONTAINER = os.getenv('AZURE_STORAGE_CONTAINER')
STORAGE_KEY = os.getenv('AZURE_STORAGE_KEY')

storage = SpeechClient(base_url=f'https://{STORAGE_ACCOUNT}.blob.core.windows.net', api_key=STORAGE_KEY, provider='azure_storage')

def archive_summary(job_id: str, summary_text: str) -> bool:
    """Upload a concise summary of a transcription job to blob storage.

    Args:
        job_id (str): Batch transcription job identifier.
        summary_text (str): Human‑readable summary.
    Returns:
        bool: True if upload succeeded, False otherwise.
    """
    blob_name = f'summaries/{job_id}.txt'
    response = storage.put(f'/blobs/{blob_name}', json={'summary': summary_text})
    return response.get('statusCode') == 201

if __name__ == '__main__':
    # Example usage (replace with real job ID and summary text)
    job_id = 'abc123-0000-1111-2222'
    summary = 'Meeting discussed Q2 revenue beats and upcoming product roadmap.'
    success = archive_summary(job_id, summary)
    print('Archive summary successful?', success)
