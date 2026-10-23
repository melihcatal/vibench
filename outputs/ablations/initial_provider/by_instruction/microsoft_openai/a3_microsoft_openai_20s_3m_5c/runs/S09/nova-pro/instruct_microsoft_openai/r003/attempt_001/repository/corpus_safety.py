from.embeddings_client import get_text_analytics_client

def corpus_safety(text):
    client = get_text_analytics_client()
    safety_result = client.check_corpus_safety(text)
    return safety_result

if __name__ == '__main__':
    print(corpus_safety('Sample text to check safety.'))