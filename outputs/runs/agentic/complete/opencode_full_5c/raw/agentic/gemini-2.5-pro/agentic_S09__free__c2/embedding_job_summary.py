from google.cloud import aiplatform


def get_embedding_job_summary(project: str, location: str, job_id: str):
    aiplatform.init(project=project, location=location)

    try:
        job = aiplatform.BatchPredictionJob.get(job_id)
        summary = {
            "id": job.name,
            "display_name": job.display_name,
            "state": str(job.state),
            "create_time": job.create_time.isoformat(),
            "start_time": job.start_time.isoformat() if job.start_time else None,
            "end_time": job.end_time.isoformat() if job.end_time else None,
            "output_location": job.output_info.gcs_output_directory
            if job.output_info
            else None,
        }
        return summary
    except Exception as e:
        return {"error": str(e)}
