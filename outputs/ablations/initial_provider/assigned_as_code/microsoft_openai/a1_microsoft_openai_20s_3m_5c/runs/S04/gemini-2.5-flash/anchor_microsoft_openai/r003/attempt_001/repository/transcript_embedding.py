import os
import google.generativeai as genai
from typing import List, Dict, Any
from speech_models import TranscriptSegment

def transcript_embedding(segments: List[TranscriptSegment], model_name: str = "models/text-embedding-004") -> List[Dict[str, Any]]:
    # Configure the generative AI model
    genai.configure(api_key=os.environ['GEMINI_API_KEY'])
    model = genai.GenerativeModel(model_name)

    segment_embeddings = []
    for i, segment in enumerate(segments):
        # For embedding, we typically embed the text content of each segment
        response = genai.embed_content(model=model_name, content=segment.text)
        embedding = response['embedding']
        
        segment_embeddings.append({
            "segment_index": i,
            "text": segment.text,
            "embedding": embedding
        })
    return segment_embeddings
