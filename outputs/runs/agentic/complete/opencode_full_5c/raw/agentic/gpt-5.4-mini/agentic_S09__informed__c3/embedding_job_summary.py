from openai import OpenAI

from embeddings_models import cosine_similarity


def embedding_job_summary(job_results):
    client = OpenAI()
    texts = [str(item.get("text", "")) for item in job_results]
    embeddings = client.embeddings.create(
        model="text-embedding-3-small", input=texts
    ).data
    vectors = [item.embedding for item in embeddings]
    scores = []
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            scores.append(cosine_similarity(vectors[i], vectors[j]))
    return {
        "item_count": len(job_results),
        "average_pairwise_similarity": sum(scores) / len(scores) if scores else 0.0,
    }
