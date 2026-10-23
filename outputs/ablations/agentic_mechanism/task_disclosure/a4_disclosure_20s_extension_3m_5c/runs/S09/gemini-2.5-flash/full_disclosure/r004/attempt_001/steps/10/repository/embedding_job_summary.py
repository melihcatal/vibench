import google.cloud.aiplatform as aiplatform

def summarize_embedding_job_results(project: str, location: str, job_id: str) -> dict:
    """
    Summarizes the results of an embedding job from Google Cloud Vertex AI.

    Args:
        project: The Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").
        job_id: The ID of the embedding job.

    Returns:
        A dictionary containing a summary of the embedding job results.
    """
    try:
        # Initialize the AI Platform Job Service Client
        client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
        job_client = aiplatform.gapic.JobServiceClient(client_options=client_options)

        # Construct the resource name for the embedding job
        job_name = job_client.batch_prediction_job_path(project, location, job_id)

        # Get the embedding job details
        embedding_job = job_client.get_batch_prediction_job(name=job_name)

        summary = {
            "job_id": embedding_job.name.split("/")[-1],
            "display_name": embedding_job.display_name,
            "state": aiplatform.JobState(embedding_job.state).name,
            "model_monitoring_config": str(embedding_job.model_monitoring_stats_anomalies),
            "create_time": embedding_job.create_time.isoformat(),
            "start_time": embedding_job.start_time.isoformat() if embedding_job.start_time else None,
            "end_time": embedding_job.end_time.isoformat() if embedding_job.end_time else None,
            "input_config": {
                "source": embedding_job.input_config.gcs_source.uris,
                "data_format": embedding_job.input_config.instances_format,
            },
            "output_config": {
                "destination": embedding_job.output_config.gcs_destination.output_uri_prefix,
                "data_format": embedding_job.output_config.predictions_format,
            },
            "error_count": embedding_job.error_count,
            "partial_failures": [str(f) for f in embedding_job.partial_failures],
        }
        return summary
    except Exception as e:
        return {"error": str(e)}

