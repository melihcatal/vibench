from typing import List, Dict
import numpy as np
from sentence_transformers import SentenceTransformer
from translation_models import TranslationResponse

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


def embed_translated_segments(
    translations: List[TranslationResponse],
) -> Dict[str, List[float]]:
    segments = []
    keys = []

    for translation in translations:
        if isinstance(translation.translated_text, str):
            segments.append(translation.translated_text)
            keys.append(translation.translated_text)
        elif isinstance(translation.translated_text, list):
            for text in translation.translated_text:
                segments.append(text)
                keys.append(text)

    embeddings = model.encode(segments, convert_to_tensor=False)
    return {key: embedding.tolist() for key, embedding in zip(keys, embeddings)}
