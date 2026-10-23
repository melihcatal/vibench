import os
import requests

# AssemblyAI Transcripts API - provide client utilities for Batch Speech-to-Text


def get_assemblyai_client():
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise RuntimeError("ASSEMBLYAI_API_KEY environment variable not set")
    return requests.Session(), api_key


# Utility to extract transcript text from AssemblyAI response


def extract_transcript(response_json):
    if response_json.get("status") != "completed":
        raise ValueError("Transcription not completed")
    return response_json["text"]
