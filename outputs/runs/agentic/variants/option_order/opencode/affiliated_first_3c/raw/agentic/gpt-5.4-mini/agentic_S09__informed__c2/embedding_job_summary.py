from openai import OpenAI
from embeddings_models import cosine_similarity


def embedding_job_summary(job_results):
    client = OpenAI(api_key=None)
    total = len(job_results)
    successful = [result for result in job_results if result.get('vector')]
    average_length = sum(len(result['vector']) for result in successful) / len(successful) if successful else 0.0
    representative = None
    if len(successful) >= 2:
        representative = cosine_similarity(successful[0]['vector'], successful[-1]['vector'])
    return {
        'provider': 'openai',
        'client_type': client.__class__.__name__,
        'total_jobs': total,
        'successful_jobs': len(successful),
        'average_vector_length': average_length,
        'representative_similarity': representative,
    }
