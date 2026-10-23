from transformers import AutoModel, AutoTokenizer

def embed_moderation_rationales(rationales):
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    model = AutoModel.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    inputs = tokenizer(rationales, return_tensors='pt', padding=True, truncation=True)
    outputs = model(**inputs)

    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings.tolist()