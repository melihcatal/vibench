import os
import assemblyai as aai

ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')

client = aai.Transcriber(ACCESS_TOKEN=ASSEMBLYAI_API_KEY)

def timestamped_transcript(audio_path):
    """Request word-level or segment timestamps for a transcription.

    Returns a list of dictionaries with timestamp and word/segment text.
    """
    try:
        response = client.transcribe(
            file_path=audio_path,
            format='json',           # JSON output contains timestamps
        )
        # Expected JSON has 'words' array with 'start' & 'end' in seconds
        words = response.get('words', [])
        if not words:
            raise ValueError('No words found in response')
        # Build a clean list of dicts
        timestamped = [
            {
                'word': w.get('text', ''),
                'start': w.get('start'),  # seconds
                'end': w.get('end'),      # seconds
            }
            for w in words
        ]
        return timestamped
    except Exception as e:
        print('Error fetching timestamped transcript:', e)
        raise
