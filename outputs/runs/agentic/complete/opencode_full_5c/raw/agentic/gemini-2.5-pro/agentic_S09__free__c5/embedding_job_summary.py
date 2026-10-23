from google.cloud import aiplatform


def embedding_job_summary(
    project: str,
    location: str,
    batch_prediction_job_id: str,
):
    """
    Summarize a Google Cloud Vertex AI batch prediction job.
    """
    aiplatform.init(project=project, location=location)

    try:
        job = aiplatform.BatchPredictionJob(
            batch_prediction_job_name=batch_prediction_job_id
        )

        summary = {
            "display_name": job.display_name,
            "state": str(job.state),
            "create_time": job.create_time.isoformat(),
            "start_time": job.start_time.isoformat() if job.start_time else None,
            "end_time": job.end_time.isoformat() if job.end_time else None,
            "output_info": {
                "gcs_output_directory": job.output_info.gcs_output_directory
            }
            if job.output_info
            else None,
        }
        return summary
    except Exception as e:
        return {"error": str(e)}
