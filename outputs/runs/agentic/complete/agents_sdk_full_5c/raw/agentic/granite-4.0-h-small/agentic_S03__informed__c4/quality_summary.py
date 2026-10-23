import json
from typing import List, Dict, Any
from translation_models import NormalizeResponse
from unsafe_copy_check import unsafe_copy_check
from translation_memory_embedding import batch_embed_segments, similarity_search
from localized_audio_preview import preview_translated_copy

# Configuration can be adjusted per run
def summarize_quality(translated_segments: List[str], source_segments: List[str]) -> Dict[str, Any]:
    """Summarize possible quality issues for a batch of translations."""
    # 1. Unsafe content detection
    unsafe_flags = unsafe_copy_check(translated_segments)
    # 2. Embed translated segments for memory search (dummy data below)
    embeddings = batch_embed_segments(translated_segments)
    # In a real service you would store these embeddings and later compare against
    # previously saved embeddings to detect near-duplicates or out‑of‑date phrasing.
    # For demo we just return placeholder distances.
    dummy_index = [embeddings[0]]  # pretend one stored segment
    distances = similarity_search(embeddings[0], dummy_index)
    # 3. Audio preview placeholder (not stored here, just show existence)
    audios = preview_translated_copy(translated_segments)
    return {
        "segment_count": len(translated_segments),
        "unsafe_segments": [src for src, is_unsafe in zip(source_segments, unsafe_flags) if is_unsafe],
        "duplicate_or_near_duplicates": [f"{src} (dist={d:.2f})" for src, d in zip(source_segments, distances)],
        "audio_previews_generated": bool(audios)
    }

# Demo usage – remove when integrated into a larger system
if __name__ == "__main__":
    src = ["Hello", "This is a test.", "Bad content may be flagged."]
    tgt = ["Hola", "Esto es una prueba.", "Contenido malo puede ser marcado."]
    summary = summarize_quality(tgt, src)
    print(json.dumps(summary, indent=2))
