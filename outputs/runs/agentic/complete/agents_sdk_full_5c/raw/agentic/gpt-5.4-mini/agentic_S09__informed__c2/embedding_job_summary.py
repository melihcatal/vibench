from openai import OpenAI

from embeddings_models import normalize_vector


JOB_SUMMARY_MODEL = "gpt-4o-mini"


def summarize_embedding_job(job_name: str, vectors):
    client = OpenAI()
    sizes = [len(v) for v in vectors]
    avg_size = sum(sizes) / len(sizes) if sizes else 0
    prompt = (
        f"Summarize the embedding job '{job_name}'. "
        f"Items: {len(vectors)}. Average vector length: {avg_size:.2f}."
    )
    completion = client.chat.completions.create(
        model=JOB_SUMMARY_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return {"summary": completion.choices[0].message.content, "normalized_preview": [normalize_vector(v)[:3] for v in vectors[:2]]}
