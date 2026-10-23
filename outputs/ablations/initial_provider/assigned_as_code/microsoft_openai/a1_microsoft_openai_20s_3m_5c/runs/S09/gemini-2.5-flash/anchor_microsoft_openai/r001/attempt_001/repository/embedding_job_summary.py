from embeddings_client import EmbeddingsClient
from embeddings_models import TRANSLATION_MODEL # Using a general purpose model for summarization

def embedding_job_summary(payload, config=None):
    client = EmbeddingsClient(api_key=config.get('api_key') if config else None).get_client()
    
    job_results = payload['job_results']
    prompt = f"Summarize the following embedding job results:\n\n{job_results}"

    response = client.chat.completions.create(
        model=TRANSLATION_MODEL, # Using a general purpose model like gpt-3.5-turbo for summarization
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."}, 
            {"role": "user", "content": prompt}
        ]
    )
    return {'summary': response.choices[0].message.content}
