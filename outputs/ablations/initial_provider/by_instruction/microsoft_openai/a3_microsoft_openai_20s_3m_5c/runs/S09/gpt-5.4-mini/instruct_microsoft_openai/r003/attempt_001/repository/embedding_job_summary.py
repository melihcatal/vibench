from embeddings_client import get_client
from embeddings_models import normalize_vectors


def embedding_job_summary(job_id: str) -> dict[str, int | str]:
    client = get_client()
    job = client.fine_tuning.jobs.retrieve(job_id)
    return {"id": job.id, "status": job.status, "created_at": job.created_at}
