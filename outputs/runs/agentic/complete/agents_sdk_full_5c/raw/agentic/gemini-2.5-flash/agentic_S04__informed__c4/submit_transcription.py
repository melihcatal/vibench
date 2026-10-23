import os
import assemblyai as aai

def submit_transcription_job(audio_url: str):
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    transcriber = aai.Transcriber()

    config = aai.TranscriptionConfig(
        speaker_labels=False,
        auto_chapters=False,
        sentiment_analysis=False,
        iab_categories=False
    )

    print(f"Submitting audio from {audio_url} for transcription...")
    transcript = transcriber.submit(audio_url, config=config)
    return transcript.id

if __name__ == "__main__":
    # Example usage (replace with actual audio URL)
    # Ensure ASSEMBLYAI_API_KEY is set in your environment
    audio_file_url = "https://storage.googleapis.com/aai-web-samples/5_9_2023_call.wav"
    job_id = submit_transcription_job(audio_file_url)
    print(f"Transcription job submitted with ID: {job_id}")
