from transformers import AutoTokenizer, AutoModel

def embed_query(query):
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
    model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
    inputs = tokenizer(query, return_tensors='pt', truncation=True, padding=True)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)

def embed_documents(documents):
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
    model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
    embeddings = []
    for doc in documents:
        inputs = tokenizer(doc, return_tensors='pt', truncation=True, padding=True)
        outputs = model(**inputs)
        embeddings.append(outputs.last_hidden_state.mean(dim=1))
    return embeddings