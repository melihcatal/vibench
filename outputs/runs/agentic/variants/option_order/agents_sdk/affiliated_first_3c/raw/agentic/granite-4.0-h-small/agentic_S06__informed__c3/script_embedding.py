import os
import dashscope

def embed_narration(script_text: str) -> List[float]:
    """Embed a narration script using DashScope's text embedding model.
    Returns a list of floats representing the embedding vector.
    """
    api_key = os.getenv('DASHSCOPE_API_KEY')
    if not api_key:
        raise RuntimeError('Missing DASHSCOPE_API_KEY environment variable')
    # DashScope's embedding endpoint
    response = dashscope.embeddings.create(
        model='text-embedding-3',          # DashScope model identifier
        input=script_text,
        dimensions=1536                    # common dimensionality; adjust if needed
    )
    # The API returns a list under 'embeddings'
    vec = response['embeddings'][0]['embedding']  # type: ignore
    return vec
