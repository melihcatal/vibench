from embeddings_client import EmbeddingsClient
from embeddings_models import TRANSLATION_MODEL

def multilingual_query_translate(payload, config=None):
    client = EmbeddingsClient(api_key=config.get('api_key') if config else None).get_client()

    query = payload['query']
    target_language = payload.get('target_language', 'English')

    prompt = f"Translate the following query into {target_language}: {query}"

    response = client.chat.completions.create(
        model=TRANSLATION_MODEL,
        messages=[
            {"role": "system", "content": f"You are a helpful assistant that translates text into {target_language}."},
            {"role": "user", "content": prompt}
        ]
    )
    return {'translated_query': response.choices[0].message.content}
