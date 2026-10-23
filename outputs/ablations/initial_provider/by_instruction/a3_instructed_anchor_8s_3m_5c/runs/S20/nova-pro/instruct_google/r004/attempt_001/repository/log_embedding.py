from sentence_transformers import SentenceTransformer

def embed_log_message(log_message):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(log_message)
    return embedding

if __name__ == '__main__':
    log_message = 'This is a log entry'
    embedding = embed_log_message(log_message)
    print(embedding)