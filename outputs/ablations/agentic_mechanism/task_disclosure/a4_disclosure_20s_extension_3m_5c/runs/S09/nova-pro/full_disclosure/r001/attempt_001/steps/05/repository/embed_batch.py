from transformers import AutoModel, AutoTokenizer
import torch

MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'

def embed_batch(texts):
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModel.from_pretrained(MODEL_NAME)

    inputs = tokenizer(texts, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings.tolist()