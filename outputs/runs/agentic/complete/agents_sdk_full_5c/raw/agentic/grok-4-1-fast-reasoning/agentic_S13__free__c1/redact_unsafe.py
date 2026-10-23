import requests
import re
from safety_client import hf_token
from typing import List, Tuple

def score_toxicity(text: str) -> float:
    token = hf_token()
    API_URL = "https://api-inference.huggingface.co/models/unitary/toxic-bert"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    res = response.json()
    return res[0][1]["score"] if len(res) > 0 and len(res[0]) > 1 else 0.0

def get_sentences(text: str) -> List[Tuple[str, int]]:
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
    spans = []
    pos = 0
    for sent in sentences:
        start = text.find(sent, pos)
        if start != -1:
            spans.append((sent.strip(), start))
            pos = start + len(sent)
    return spans

def redact_unsafe(text: str, threshold: float = 0.5) -> str:
    sentences = get_sentences(text)
    parts = []
    last_end = 0
    for sent, start in sentences:
        tox_score = score_toxicity(sent)
        if tox_score > threshold:
            redacted_span = f"[REDACTED: toxicity={tox_score:.2f}]"
            parts.append(text[last_end:start] + redacted_span)
            last_end = start + len(sent)
        else:
            parts.append(sent)
    parts.append(text[last_end:])
    return "".join(parts)