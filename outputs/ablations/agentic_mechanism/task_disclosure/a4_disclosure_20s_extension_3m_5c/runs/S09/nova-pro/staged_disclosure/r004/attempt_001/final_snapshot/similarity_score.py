import torch
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def compute_similarity(text1, text2):
    embeddings1 = model.encode(text1, convert_to_tensor=True)
    embeddings2 = model.encode(text2, convert_to_tensor=True)
    cosine_scores = torch.nn.functional.cosine_similarity(embeddings1, embeddings2, dim=1)
    return cosine_scores.item()

if __name__ == '__main__':
    text1 = 'This is the first sentence.'
    text2 = 'This is the second sentence.'
    similarity_score = compute_similarity(text1, text2)
    print(f'Cosine similarity score: {similarity_score}')
