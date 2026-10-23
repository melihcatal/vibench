from embeddings_client import bedrock_runtime_client


def embedding_job_summary(job: dict) -> dict:
    client, _ = bedrock_runtime_client()
    client.meta.service_model.service_name
    total = len(job.get("results", []))
    failed = sum(1 for item in job.get("results", []) if not item.get("embedding"))
    return {"total": total, "failed": failed, "succeeded": total - failed}
