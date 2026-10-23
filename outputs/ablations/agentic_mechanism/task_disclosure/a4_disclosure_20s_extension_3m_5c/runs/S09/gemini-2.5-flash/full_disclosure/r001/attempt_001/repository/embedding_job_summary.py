from google.cloud import aiplatform

def summarize_embedding_job_results(job_id: str, project: str, location: str):
    """
    Summarizes the results of a Google Cloud Vertex AI embedding job.

    Args:
        job_id: The ID of the embedding job.
        project: The Google Cloud project ID.
        location: The Google Cloud region where the job was run (e.g., "us-central1").

    Returns:
        A dictionary summarizing the job results, or None if the job is not found.
    """
    try:
        # Initialize the AI Platform client
        aiplatform.init(project=project, location=location)

        # Get the CustomJob object (embedding jobs are often run as CustomJobs or BatchPredictionJobs)
        # For simplicity, we'll assume it's a CustomJob that produced embeddings.
        # In a real-world scenario, you might need to check if it's a BatchPredictionJob
        # if you're using managed embedding services.
        job = aiplatform.CustomJob.get(job_id)

        summary = {
            "job_id": job.name,
            "display_name": job.display_name,
            "state": job.state.name,
            "create_time": job.create_time.isoformat(),
            "start_time": job.start_time.isoformat() if job.start_time else None,
            "end_time": job.end_time.isoformat() if job.end_time else None,
            "errors": [str(error) for error in job.error.message] if job.error else [],
            "uri": f"https://console.cloud.google.com/vertex-ai/locations/{location}/training/{job.name.split('/')[-1]}?project={project}"
        }
        return summary
    except Exception as e:
        print(f"Error summarizing embedding job {job_id}: {e}")
        return None

