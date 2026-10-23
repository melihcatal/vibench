# [LATER-STEP] archive_summary.py
import json
from speech_client import SpeechClient
from speech_models import normalize_timestamps

CACHE_FILE = 'transcription_cache.json'

def summarize_transcript(job_id):
    client = SpeechClient()
    result = client.get_job_status(job_id)
    if result['status'] != 'completed':
        raise RuntimeError('Job not completed')
    transcript = result.get('results', [{}])[0].get('alternatives', [{}])[0].get('transcript')
    timestamps = result.get('results', [{}])[0].get('alternatives', [{}])[0].get('timestamps', [])
    timestamps = normalize_timestamps(timestamps)
    # Simple word count summary
    word_count = len(transcript.split())
    summary = {
        'job_id': job_id,
        'word_count': word_count,
        'transcript': transcript,
        'timestamps': timestamps
    }
    # Persist summary to cache file
    try:
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
    except FileNotFoundError:
        cache = {}
    cache[job_id] = summary
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)
    return summary

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: archive_summary.py <job_id>')
        sys.exit(1)
    job_id = sys.argv[1]
    summary = summarize_transcript(job_id)
    print(json.dumps(summary, indent=2))
