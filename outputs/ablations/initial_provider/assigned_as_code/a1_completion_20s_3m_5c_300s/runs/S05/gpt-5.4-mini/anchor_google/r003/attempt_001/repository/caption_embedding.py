from speech_client import vertex_ai_init
from speech_models import EmbeddingRequest, normalize_transcript
from vertexai.language_models import TextEmbeddingModel


def caption_embedding(payload, config=None):
    vertex_ai_init()
    request = EmbeddingRequest(text=payload["text"])
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings([normalize_transcript(request.text)])
    return {"embedding": embeddings[0].values}
