from transformers import AutoModel, AutoTokenizer

def embed_segment(segment: str, model_name: str = 'sentence-transformers/all-MiniLM-L6-v2') -> list:
    model = AutoModel.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    inputs = tokenizer(segment, return_tensors='pt', truncation=True, padding=True)
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()
    return embeddings

if __name__ == '__main__':
    segment = 'This is a sample segment to be embedded.'
    embeddings = embed_segment(segment)
    print(f'Embeddings: {embeddings}')
