import google.generativeai as genai

def moderation_reason_embedding(payload, config=None):
    config = config or {}
    genai.configure(api_key=config['api_key'])

    # Using a specific embedding model
    model_name = config.get('embedding_model', 'text-embedding-004')

    text_to_embed = payload['rationale']

    try:
        response = genai.embed_content(model=model_name, content=text_to_embed)
        embedding = response['embedding']
    except Exception as e:
        embedding = f"Error generating embedding: {e}"

    return {'rationale': text_to_embed, 'embedding': embedding}