import assemblyai as aai
from speech_client import get_assemblyai_client
from speech_models import get_audio_url_from_env

def request_diarized_transcript(audio_url: str) -> aai.Transcript:
    """
    Submits an audio file for transcription with speaker diarization enabled
    using AssemblyAI.

    Args:
        audio_url: The URL of the audio file to transcribe.

    Returns:
        The AssemblyAI Transcript object which will contain diarization results
        once the job is completed.
    """
    client = get_assemblyai_client()

    config = aai.TranscriptionConfig(
        speaker_diarization=True, 
        language_code="en_us"
    )
    transcriber = aai.Transcriber(config=config)
    
    print(f"Submitting transcription with diarization for audio: {audio_url}")
    transcript = transcriber.submit(audio_url)
    
    if transcript and transcript.id:
        print(f"Transcription job submitted with ID: {transcript.id}. Diarization enabled.")
        return transcript
    else:
        raise Exception("Failed to submit transcription job with diarization.")

if __name__ == "__main__":
    import time
    try:
        audio_file_url = get_audio_url_from_env()
        transcript_obj = request_diarized_transcript(audio_file_url)

        print("\nPolling for completion...")
        while transcript_obj.status not in [aai.TranscriptStatus.completed, aai.TranscriptStatus.error]:
            time.sleep(5)
            transcript_obj = get_assemblyai_client().transcripts.get(transcript_obj.id)
            print(f"Current status: {transcript_obj.status}")
        
        if transcript_obj.status == aai.TranscriptStatus.error:
            raise Exception(f"Transcription job failed: {transcript_obj.error}")

        print("\n--- Diarized Transcript ---")
        for utterance in transcript_obj.utterances:
            print(f"Speaker {utterance.speaker}: {utterance.text}")

    except Exception as e:
        print(f"Error: {e}")
