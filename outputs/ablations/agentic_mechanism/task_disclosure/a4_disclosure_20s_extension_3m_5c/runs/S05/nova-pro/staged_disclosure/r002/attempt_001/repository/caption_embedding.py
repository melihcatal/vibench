import torch
from transformers import AutoTokenizer, AutoModel

def embed_caption_chunks(caption_chunks):
    model_name = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    embeddings = []
    for chunk in caption_chunks:
        inputs = tokenizer(chunk, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()
        embeddings.append(embedding)

    return embeddings
