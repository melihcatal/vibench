import os
import google.generativeai as genai
from speech_models import TranscriptSegment
from typing import List, Dict

def embed_transcript_segments(segments: List[TranscriptSegment]) -> List[Dict[str, List[float]]]:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    embedded_segments = []
    for segment in segments:
        response = genai.embed_content(
            model="models/embedding-001",
            content=segment.text,
            task_type="RETRIEVAL_DOCUMENT"
        )
        embedded_segments.append({"segment_id": segment.id, "embedding": response["embedding"]})
    return embedded_segments
