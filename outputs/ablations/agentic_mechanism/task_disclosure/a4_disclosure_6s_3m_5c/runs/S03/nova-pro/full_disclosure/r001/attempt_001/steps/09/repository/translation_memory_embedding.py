import torch
from transformers import AutoModel, AutoTokenizer

class TranslationMemoryEmbedding:
    def __init__(self):
        self.model_name = 'sentence-transformers/all-MiniLM-L6-v2'
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)

    def embed(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings.numpy()

if __name__ == '__main__':
    embedding_client = TranslationMemoryEmbedding()
    sample_text = 'This is a sample text to be embedded.'
    embeddings = embedding_client.embed(sample_text)
    print(embeddings)