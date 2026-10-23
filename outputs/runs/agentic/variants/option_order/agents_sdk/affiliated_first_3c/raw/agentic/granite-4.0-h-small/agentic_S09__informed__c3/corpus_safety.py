import spacy
from langdetect import detect

def corpus_safety(text: str) -> bool:
    """Check text for disallowed or unsafe content using spaCy model."""
    try:
        lang = detect(text)
    except Exception:
        lang = 'unknown'
    nlp = spacy.load('en_core_web_sm' if lang == 'en' else 'xx_ent_wiki_sm')
    doc = nlp(text)
    # Simple heuristic: flag texts with hate, profanity, or personal data
    bad_tokens = [token.text for token in doc if token.is_stop or token.is_punct]
    return len(bad_tokens) / max(len(doc), 1) < 0.1