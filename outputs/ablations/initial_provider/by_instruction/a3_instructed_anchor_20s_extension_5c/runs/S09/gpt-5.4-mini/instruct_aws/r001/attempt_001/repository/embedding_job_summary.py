import json

import boto3


def embedding_job_summary(job_id):
    client = boto3.client("bedrock")
    job = client.get_model_customization_job(jobIdentifier=job_id)
    return json.dumps({"job_id": job_id, "status": job.get("status"), "output": job.get("outputDataConfig", {})})
