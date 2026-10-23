from sentence_transformers import SentenceTransformer
from speech_models import FinalResult

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_caption(result: FinalResult) -> list[float]:
    text = result.transcript
    embedding = model.encode(text, convert_to_tensor=False)
    return embedding.tolist()