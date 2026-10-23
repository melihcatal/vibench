import os
from speech_client import get_speech_client

def diarized_transcript(file_path, num_speakers=2):
    """Request speaker diarization for a recorded meeting.
    Returns the transcript with speaker labels.
    """
    client = get_speech_client()
    # AssemblyAI supports speaker labels via 'speaker_labels=True'
    response = client.transcribe(file_path, speaker_labels=True, num_speakers=num_speakers)
    transcript = response.get('transcript', '')
    print(f"Diarized transcript (requested {num_speakers} speakers):\n{transcript}")
    return transcript

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: diarized_transcript.py <path_to_audio_file>')
        sys.exit(1)
    path = sys.argv[1]
    diarized_transcript(path)
