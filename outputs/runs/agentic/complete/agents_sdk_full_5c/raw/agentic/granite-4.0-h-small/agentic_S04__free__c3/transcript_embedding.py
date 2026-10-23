import os
import json
import requests
from speech_client import get_batch_client
from speech_models import BatchTranscriptionResult

# Required environment variables for Azure Cognitive Services Speech & Azure OpenAI
# AZURE_SPEECH_BATCH_KEY, AZURE_SPEECH_BATCH_REGION, AZURE_OPENAI_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_EMBEDDING_DEPLOYMENT, AZURE_OPENAI_EMBEDDING_MODEL

def embed_transcript(transcript: BatchTranscriptionResult) -> List[Dict[str, Any]]:
    """Generate embeddings for each transcript segment.

    Sends segment content to Azure OpenAI embedding model and returns list of embedding dicts.
    
    Args:
        transcript (BatchTranscriptionResult): Azure Speech-to-Text result JSON.

    Returns:
        list: Each entry contains segment_id, speaker_labels, start_sec, text, embedding (list[float]).
    """
    client = get_batch_client()
    endpoint = client.endpoint
    # Translator / Speech variables already set by caller environment
    embedding_key = os.getenv("AZURE_OPENAI_KEY")
    embedding_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    model = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL")
    if not all([embedding_key, embedding_endpoint, deployment, model]):
        raise RuntimeError(
            "Set AZURE_OPENAI_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_EMBEDDING_DEPLOYMENT, AZURE_OPENAI_EMBEDDING_MODEL"
        )

    # Build request payload: list of texts
    segments = transcript.get("results", [{}])[0].get("segments", [])
    embeddings = []
    for seg in segments:
        seg_id = seg.get("segment_id")
        speaker = seg.get("speaker_labels", [])
        start_ms = seg.get("audio_start_time_ms")
        start_sec = start_ms / 1000.0 if start_ms else 0.0
        text = seg.get("content", "")
        payload = {
            "inputs": [{"text": text}]
        }
        # OpenAI API uses /embeddings route
        url = f"{embedding_endpoint}/openai/deployments/{deployment}/embeddings?api-version=2023-05-15"
        headers = {
            "api-key": embedding_key,
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        # OpenAI returns data.data[0].embedding as list of floats
        embedding = data["data"][0]["embedding"]
        embeddings.append(
            {
                "segment_id": seg_id,
                "speaker_labels": speaker,
                "audio_start_sec": start_sec,
                "text": text,
                "embedding": embedding
            }
        )
    return embeddings

# Example CLI usage – embed a saved transcription result file
if __name__ == "__main__":
    import sys, json
    if len(sys.argv) != 2:
        print("Usage: python transcript_embedding.py <result_json_file>")
        sys.exit(1)
    file_path = sys.argv[1]
    with open(file_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    embeddings = embed_transcript(raw)
    print(json.dumps(embeddings, ensure_ascii=False, indent=2))
