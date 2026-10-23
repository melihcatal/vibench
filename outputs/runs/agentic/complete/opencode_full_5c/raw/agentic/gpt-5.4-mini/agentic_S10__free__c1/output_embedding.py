from model_client import get_client, load_config
from model_models import TextRequest


def output_embedding(request: TextRequest):
    cfg = load_config(request.model)
    client = get_client(cfg)
    return client.embeddings.create(model="text-embedding-3-large", input=request.text)
