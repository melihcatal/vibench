from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(text1, text2):
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    inputs1 = tokenizer(text1, return_tensors='pt', truncation=True, padding=True)
    inputs2 = tokenizer(text2, return_tensors='pt', truncation=True, padding=True)

    with torch.no_grad():
        outputs1 = model(**inputs1)
        outputs2 = model(**inputs2)

    embedding1 = outputs1.last_hidden_state.mean(dim=1).squeeze().numpy()
    embedding2 = outputs2.last_hidden_state.mean(dim=1).squeeze().numpy()

    similarity_score = cosine_similarity([embedding1], [embedding2])[0][0]
    return similarity_score

if __name__ == '__main__':
    text1 = 'This is the first text.'
    text2 = 'This is the second text.'
    similarity = compute_similarity(text1, text2)
    print(f'Cosine similarity: {similarity}')
