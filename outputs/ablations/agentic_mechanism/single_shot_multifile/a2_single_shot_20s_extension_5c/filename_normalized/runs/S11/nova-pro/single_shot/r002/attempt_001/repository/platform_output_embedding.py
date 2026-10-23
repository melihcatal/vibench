from sentence_transformers import SentenceTransformer

def embed_output(output_text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(output_text)
    return embedding