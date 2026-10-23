from transformers import AutoModel, AutoTokenizer

def embed_secret_audit_notes(notes):
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    model = AutoModel.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    inputs = tokenizer(notes, return_tensors='pt', padding=True, truncation=True)
    outputs = model(**inputs)

    embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()
    return embeddings