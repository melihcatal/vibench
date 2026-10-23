MODEL_EMBED = "text-embedding-3-small"

def normalize_text(text: str) -> str:
    return text.strip()

def normalize_texts(texts: list[str]) -> list[str]:
    return [normalize_text(t) for t in texts if normalize_text(t)]