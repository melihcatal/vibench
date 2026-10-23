from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_log_message(message):
    embedding = model.encode(message)
    return embedding

log_message = 'This is a log message to be embedded'

embedding = embed_log_message(log_message)
print(embedding)