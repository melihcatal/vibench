import re
from openai import OpenAI
from embeddings_client import embedding_model


def corpus_safety(texts):
    client = OpenAI()
    flagged = []
    for text in texts:
        if re.search(r'\b(ssn|password|secret|api key)\b', str(text), re.I):
            flagged.append({'text': text, 'reason': 'sensitive_keyword'})
    return {'provider': 'openai', 'model': embedding_model(), 'flagged': flagged, 'count': len(flagged)}
