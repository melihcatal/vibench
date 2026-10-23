import os
import json
import os
import torch
from transformers import AutoTokenizer, AutoModel
from speech_client import BatchSpeechClient
from speech_models import TimestampedTranscript

# ------------------------------------------------------------
# transcript_embedding.py
# Embed transcript segments for semantic retrieval
# ------------------------------------------------------------

def embed_transcript(job_id: str, model_name: str = "sentence-transformers/all-MiniLM-L12-v2") -> list:
    """Fetch a timestamped transcript and embed each segment using a Sentence‑Transformer model.

    Returns a list of dicts: {"word": ..., "embedding": list[float]}.
    """
    client = BatchSpeechClient()
    results = client.get_transcription_results(job_id)
    # The results endpoint used above does not include timestamps; for demo we embed only words.
    words = results.get("results", [])
    # Load tokenizer & model (cached locally)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    embeddings = []
    for w in words:
        inputs = tokenizer(w, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
            emb = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()
        embeddings.append({"word": w, "embedding": emb})
    return embeddings

# Example usage (run as script)
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Embed a batch transcription for retrieval.")
    parser.add_argument("job_id", help="Transcription job ID.")
    parser.add_argument("--model", default="sentence-transformers/all-MiniLM-L12-v2", help="HF model name for embeddings.")
    args = parser.parse_args()
    embs = embed_transcript(args.job_id, args.model)
    print(json.dumps(embs, indent=2))
