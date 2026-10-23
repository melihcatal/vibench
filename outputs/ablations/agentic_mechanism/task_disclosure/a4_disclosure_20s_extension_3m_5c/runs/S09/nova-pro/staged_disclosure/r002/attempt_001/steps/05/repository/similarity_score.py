from transformers import AutoModel, AutoTokenizer
from scipy.spatial.distance import cosine

# Load model and tokenizer
model_name = 'sentence-transformers/all-MiniLM-L6-v2'
model = AutoModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def compute_cosine_similarity(text1, text2):
    # Tokenize and encode sequences in a batch
    encoded_input = tokenizer(text1, text2, padding=True, truncation=True, return_tensors='pt')
    
    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)
    
    # Pool the output (e.g., mean pooling)
    token_embeddings = model_output.last_hidden_state
    input_mask_expanded = encoded_input['attention_mask'].unsqueeze(-1).expand(token_embeddings.size()).float()
    token_embeddings[input_mask_expanded == 0] = 0
    sum_embeddings = torch.sum(token_embeddings, 1)
    sum_mask = input_mask_expanded.sum(1, keepdim=True)
    mean_embeddings = sum_embeddings / sum_mask
    
    # Compute cosine similarity
    similarity = 1 - cosine(mean_embeddings[0], mean_embeddings[1])
    return similarity.item()

# Example usage
text1 = 'This is the first sentence.'
text2 = 'This is the second sentence.'
similarity = compute_cosine_similarity(text1, text2)
print(f'Cosine similarity: {similarity}')