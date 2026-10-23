import os
from gtts import gTTS
from pathlib import Path
from embeddings_models import normalize_embedding

def retrieval_audio_brief(search_results, output_file="brief.mp3"):
    """Generate a spoken brief from retrieved search results using Google Text-to-Speech."""
    # Simple concatenation of titles (placeholder)
    brief_text = "Found documents: " + ", ".join([r['title'] for r in search_results])
    tts = gTTS(text=brief_text, lang='en')
    Path(output_file).write_bytes(tts.read())
    return output_file
