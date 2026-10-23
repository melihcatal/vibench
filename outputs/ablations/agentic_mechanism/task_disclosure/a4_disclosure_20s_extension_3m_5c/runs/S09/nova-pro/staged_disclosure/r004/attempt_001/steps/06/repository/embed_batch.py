import os
from transformers import AutoModel, AutoTokenizer

# Set your Hugging Face API key
HUGGING_FACE_API_KEY = os.getenv('HUGGING_FACE_API_KEY')

# Load the model and tokenizer
model_name = 'sentence-transformers/all-MiniLM-L6-v2'
model = AutoModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def generate_embeddings(texts):
    inputs = tokenizer(texts, return_tensors='pt', padding=True, truncation=True)
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings.tolist()

if __name__ == '__main__':
    texts = ['This is a sample text.', 'Another text for embedding.']
    embeddings = generate_embeddings(texts)
    print(embeddings)