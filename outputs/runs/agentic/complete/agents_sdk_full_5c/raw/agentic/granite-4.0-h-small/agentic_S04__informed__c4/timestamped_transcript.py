import os
from speech_client import get_speech_client

def timestamped_transcript(file_path):
    """Request word timestamps from a transcription result.
    Returns the transcript with timecodes for each word/segment.
    """
    client = get_speech_client()
    response = client.transcribe(file_path, timestamps=True)
    result = response.get('result', [])
    transcript = []
    for item in result:
        # Each item contains 'alternatives' with 'transcript' and 'timestamps'
        words = item.get('alternatives', [{}])[0]
        transcript_text = words.get('transcript', '')
        timecodes = words.get('timestamps', [])
        # Combine text with timecodes for display
        line = f"{transcript_text} (timestamps: {timecodes})"
        transcript.append(line)
    full_text = '\n'.join(transcript)
    print(f"Timestamped transcript for {file_path}:\n{full_text}")
    return full_text

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: timestamped_transcript.py <path_to_audio_file>')
        sys.exit(1)
    path = sys.argv[1]
    timestamped_transcript(path)
