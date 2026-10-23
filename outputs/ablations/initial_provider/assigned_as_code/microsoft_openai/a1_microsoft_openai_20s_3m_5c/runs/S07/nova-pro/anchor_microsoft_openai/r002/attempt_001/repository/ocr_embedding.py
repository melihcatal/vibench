from sentence_transformers import SentenceTransformer

def embed_document_sections(text):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embeddings = model.encode(text.split('\n'))
    return embeddings