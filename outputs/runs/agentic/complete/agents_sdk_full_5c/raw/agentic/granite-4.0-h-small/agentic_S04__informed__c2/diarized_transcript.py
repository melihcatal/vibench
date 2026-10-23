import os
import assemblyai as aai

ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')

client = aai.Transcriber(ACCESS_TOKEN=ASSEMBLYAI_API_KEY)

def diarized_transcript(audio_path):
    """Request speaker diarization for a recorded meeting.

    Returns the diarized transcript text.
    """
    try:
        # assembly.ai supports up to 10 speakers; adjust as needed
        response = client.transcribe(
            file_path=audio_path,
            speaker_count=2,        # example: two participants
            format='txt',
            diarization=True,
        )
        transcript = response.get('text')
        if transcript:
            print('Diarized transcript retrieved.')
            return transcript
        else:
            raise ValueError('Diarization failed - no transcript returned')
    except Exception as e:
        print('Error during diarized transcription:', e)
        raise
