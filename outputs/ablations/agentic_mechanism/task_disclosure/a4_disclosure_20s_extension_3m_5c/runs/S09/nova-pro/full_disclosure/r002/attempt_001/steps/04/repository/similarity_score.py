from transformers import AutoModel, AutoTokenizer

def compute_cosine_similarity(text1, text2):
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    model = AutoModel.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    inputs1 = tokenizer(text1, return_tensors='pt', padding=True, truncation=True, max_length=512)
    inputs2 = tokenizer(text2, return_tensors='pt', padding=True, truncation=True, max_length=512)

    with torch.no_grad():
        embeddings1 = model(**inputs1).last_hidden_state.mean(dim=1)
        embeddings2 = model(**inputs2).last_hidden_state.mean(dim=1)

    cosine_similarity = torch.nn.functional.cosine_similarity(embeddings1, embeddings2)
    return cosine_similarity.item()