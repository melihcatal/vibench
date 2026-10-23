import os
from google.cloud import aiplatform


def get_batch_prediction_job_summary(job_id: str) -> dict:
    """
    Summarizes an embedding batch prediction job from Google Cloud's Vertex AI.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    aiplatform.init(project=project_id, location=location)

    try:
        job = aiplatform.BatchPredictionJob(batch_prediction_job_name=job_id)
        summary = {
            "resource_name": job.resource_name,
            "display_name": job.display_name,
            "state": str(job.state),
            "create_time": job.create_time.isoformat(),
            "start_time": job.start_time.isoformat() if job.start_time else None,
            "end_time": job.end_time.isoformat() if job.end_time else None,
            "error": job.error,
        }
        return summary
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    # Replace with a real job ID from your GCP project to test
    # e.g. "projects/1234567890/locations/us-central1/batchPredictionJobs/9876543210"
    example_job_id = os.getenv(
        "VERTEX_AI_BATCH_JOB_ID",
        "projects/your-project/locations/us-central1/batchPredictionJobs/12345",
    )
    job_summary = get_batch_prediction_job_summary(example_job_id)
    print(job_summary)
