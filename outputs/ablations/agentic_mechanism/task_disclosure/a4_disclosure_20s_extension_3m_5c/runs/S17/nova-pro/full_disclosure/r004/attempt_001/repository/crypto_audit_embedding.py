import os
from transformers import AutoModel, AutoTokenizer

# Hugging Face model for text embedding
MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'

class CryptoAuditEmbedder:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModel.from_pretrained(MODEL_NAME)

    def embed(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings.detach().numpy()

if __name__ == '__main__':
    audit_notes = 'Sample crypto audit note for embedding.'
    embedder = CryptoAuditEmbedder()
    embeddings = embedder.embed(audit_notes)
    print(f'Embeddings: {embeddings}')
