import os
import requests
import numpy as np
import sentence_transformers

# provider: Sentence Transformers (hosted Hugging Face model inference)
MODEL_NAME = "all-MiniLM-L12-v2"
model = sentence_transformers.SentenceTransformer(MODEL_NAME)


def transcript_embedding(transcripts):
    """
    Embeds a list of transcript strings using Sentence Transformers.
    Returns a list of numpy vectors.
    """
    embeddings = model.encode(transcripts, convert_to_numpy=True)
    return embeddings
