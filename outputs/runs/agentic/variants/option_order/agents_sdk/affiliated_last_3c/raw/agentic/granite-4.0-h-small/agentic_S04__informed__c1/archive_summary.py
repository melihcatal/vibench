import os
import json
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.nlp.text_summarization import Summarization
from speech_client import SpeechClient
from speech_models import TranscriptionResult

# Provider credentials (env vars or config)
WATSONX_API_KEY = os.getenv('WATSONX_API_KEY')
WATSONX_PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')
SUMMARIZATION_MODEL = os.getenv('SUMMARIZATION_MODEL', 'ibm/granite-13b-instruct-v2')

# Initialize Watsonx client for summarization
client = APIClient(api_key=WATSONX_API_KEY, project_id=WATSONX_PROJECT_ID)
summary_service = Summarization(client=client)

def summarize_transcript(transcript: str, model: str = SUMMARIZATION_MODEL) -> str:
    """Summarize full transcript using watsonx text summarization API."""
    print("Calling watsonx summarization service...")
    response = summary_service.summarize(text=transcript, model_id=model)
    # Expected response contains \"summary\"
    summary = response.get('summary', '')
    print("Generated summary:")
    print(summary)
    return summary


def main(file_path: str):
    client = SpeechClient()
    # Submit batch transcription job
    job_id = client.transcribe(file_path, api_key=os.getenv('ASSEMBLYAI_API_KEY'))
    from poll_transcription import poll_transcription
    segments = poll_transcription(job_id)
    full_transcript = \" \".join([seg['text'] for seg in segments])
    summary = summarize_transcript(full_transcript)
    return summary

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Submit audio, transcribe, then produce summary.")
    parser.add_argument("file", help="Path to audio file.")
    args = parser.parse_args()
    summarize_transcript(args.file)
