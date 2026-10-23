from sentence_transformers import SentenceTransformer

def embed_log_message(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(text)
    return embedding

if __name__ == '__main__':
    log_message = 'This is a log message to be embedded'
    embedding = embed_log_message(log_message)
    print(embedding)