from transformers import AutoModel, AutoTokenizer
import torch

def compute_similarity(text1, text2):
    model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    model = AutoModel.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    inputs1 = tokenizer(text1, return_tensors='pt', padding=True, truncation=True)
    inputs2 = tokenizer(text2, return_tensors='pt', padding=True, truncation=True)

    with torch.no_grad():
        outputs1 = model(**inputs1)
        outputs2 = model(**inputs2)

    embedding1 = outputs1.last_hidden_state.mean(dim=1).squeeze()
    embedding2 = outputs2.last_hidden_state.mean(dim=1).squeeze()

    cosine_similarity = torch.nn.functional.cosine_similarity(embedding1, embedding2)
    return cosine_similarity.item()

if __name__ == '__main__':
    text1 = 'This is the first sentence.'
    text2 = 'This is the second sentence.'
    similarity_score = compute_similarity(text1, text2)
    print(f'Cosine similarity: {similarity_score}')
