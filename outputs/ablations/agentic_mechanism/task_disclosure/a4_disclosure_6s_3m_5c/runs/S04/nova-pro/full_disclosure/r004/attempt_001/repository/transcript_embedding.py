import os
from transformers import AutoModel, AutoTokenizer

class TranscriptEmbedder:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)

    def embed_segment(self, segment):
        inputs = self.tokenizer(segment, return_tensors='pt', truncation=True, padding=True)
        outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings.detach().numpy()

    def embed_transcript(self, transcript):
        segments = transcript.split('\n')
        embeddings = [self.embed_segment(segment) for segment in segments]
        return embeddings

if __name__ == '__main__':
    transcript = 'This is a sample transcript segment. Here is another segment.'
    embedder = TranscriptEmbedder()
    embeddings = embedder.embed_transcript(transcript)
    print(embeddings)