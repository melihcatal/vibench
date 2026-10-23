import os
import json
from google.cloud import genai
from speech_client import SpeechClient
from speech_models import TranscriptionResult

# Provider credentials (env vars or config)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'embed-003')

genai.configure(api_key=GOOGLE_API_KEY)
# Initialize embedding service (Google Gemini Embeddings)
embedding_client = genai.Service.from_pretrained(EMBEDDING_MODEL)

def embed_transcript(transcript: str) -> str:
    """Generate embedding for entire transcript."""
    # Google Gemini Embeddings API expects a list of strings; pass single transcript as one element
    response = embedding_client.embed_content(contents=[transcript])
    # Response contains ndarray of floats; convert to JSON-serializable list
    embedding = response[0].embedding.tolist()
    embedding_str = json.dumps(embedding)
    return embedding_str


def main(file_path: str):
    client = SpeechClient()
    job_id = client.transcribe(file_path, api_key=os.getenv('ASSEMBLYAI_API_KEY'))
    from poll_transcription import poll_transcription
    segments = poll_transcription(job_id)
    full_transcript = \" \".join([seg['text'] for seg in segments])
    embedding = embed_transcript(full_transcript)
    print("Embedding (JSON):", embedding)
    return embedding

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Submit audio, transcribe, then embed transcript.")
    parser.add_argument("file", help="Path to audio file.")
    args = parser.parse_args()
    embed_transcript(args.file)
