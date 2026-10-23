def check_corpus_safety(text):
    return 'SAFE' if 'unsafe' not in text.lower() else 'UNSAFE'