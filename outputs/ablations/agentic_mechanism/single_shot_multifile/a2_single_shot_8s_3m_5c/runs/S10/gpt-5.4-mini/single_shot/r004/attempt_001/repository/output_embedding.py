from typing import List, Optional
from model_client import get_openai_client, select_text_model


def output_embedding(text: str, model: Optional[str] = None) -> List[float]:
    client = get_openai_client()
    model_id = select_text_model(model=model, task="embedding")
    response = client.embeddings.create(
        model=model_id,
        input=text,
    )
    return list(response.data[0].embedding)
