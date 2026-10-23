import os
from sentence_transformers import SentenceTransformer

def platform_output_embedding(output):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embedding = model.encode(output)
    return embedding

model = select_platform_resource()
for output in stream_platform_generation(model):
    embedding = platform_output_embedding(output)
    print(embedding)