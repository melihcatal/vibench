from model_client import embed_texts
from model_models import get_input_text


def output_embedding(payload, config=None):
    text = get_input_text(payload)
    response = embed_texts([text], config=config)
    return {'embedding': response.data[0].embedding if response.data else []}
