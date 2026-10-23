import torch
from transformers import AutoModel, AutoTokenizer

class TranslationMemoryEmbedder:
    def __init__(self):
        self.model_name = 'sentence-transformers/all-MiniLM-L6-v2'
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)

    def embed(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings.numpy()

if __name__ == '__main__':
    embedder = TranslationMemoryEmbedder()
    example_text = 'This is an example text to embed.'
    embedding = embedder.embed(example_text)
    print(embedding)