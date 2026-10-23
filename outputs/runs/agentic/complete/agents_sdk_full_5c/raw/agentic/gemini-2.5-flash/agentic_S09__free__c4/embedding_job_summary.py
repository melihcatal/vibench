import os
from google.cloud import aiplatform
from google.cloud.aiplatform_v1.services import job_service
from google.cloud.aiplatform_v1.types import CustomJob, BatchPredictionJob
from google.cloud.aiplatform_v1.types.job_state import JobState
from google.api_core.exceptions import NotFound

def summarize_embedding_job_results(
    project_id: str, 
    location: str, 
    job_id: str, 
    job_type: str = "batch_prediction" # or "custom_job"
) -> dict:
    """
    Summarizes the results or status of an embedding job from Google Cloud Vertex AI.
    This example focuses on BatchPredictionJob, which is commonly used for large-scale embeddings.
    """
    client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    client = job_service.JobServiceClient(client_options=client_options)

    job_name_prefix = f"projects/{project_id}/locations/{location}"
    
    summary = {"job_id": job_id, "status": "NOT_FOUND", "details": "Job not found or inaccessible."}

    try:
        if job_type == "batch_prediction":
            job_name = f"{job_name_prefix}/batchPredictionJobs/{job_id}"
            job = client.get_batch_prediction_job(name=job_name)
            summary["status"] = JobState(job.state).name
            summary["details"] = {
                "display_name": job.display_name,
                "model_display_name": job.model_display_name,
                "input_config_gcs_source": [source.uris for source in job.input_config.gcs_source.uris],
                "output_config_gcs_destination": job.output_config.gcs_destination.output_uri_prefix,
                "create_time": job.create_time.isoformat(),
                "start_time": job.start_time.isoformat() if job.start_time else "N/A",
                "end_time": job.end_time.isoformat() if job.end_time else "N/A",
                "error": job.error.message if job.error else "N/A",
                "completion_statistics": {
                    "successful_count": job.output_info.successful_count,
                    "failed_count": job.output_info.failed_count,
                    "skipped_count": job.output_info.skipped_count,
                }
            }
        elif job_type == "custom_job":
            job_name = f"{job_name_prefix}/customJobs/{job_id}"
            job = client.get_custom_job(name=job_name)
            summary["status"] = JobState(job.state).name
            summary["details"] = {
                "display_name": job.display_name,
                "worker_pool_specs": [str(spec) for spec in job.worker_pool_specs],
                "create_time": job.create_time.isoformat(),
                "start_time": job.start_time.isoformat() if job.start_time else "N/A",
                "end_time": job.end_time.isoformat() if job.end_time else "N/A",
                "error": job.error.message if job.error else "N/A",
            }
        else:
            summary["status"] = "INVALID_JOB_TYPE"
            summary["details"] = f"Unsupported job type: {job_type}. Supported types are 'batch_prediction' and 'custom_job'."

    except NotFound:
        pass # Summary already initialized to NOT_FOUND
    except Exception as e:
        summary["status"] = "ERROR"
        summary["details"] = f"An error occurred: {str(e)}"
    
    return summary

if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        # NOTE: Replace with a real Batch Prediction Job ID from your Vertex AI project.
        # This example won't work without an actual job ID.
        # You can find job IDs in the Vertex AI console under "Batch predictions" or "Custom jobs".
        mock_job_id = "your-actual-batch-prediction-job-id" 
        
        print(f"Attempting to summarize Batch Prediction Job ID: {mock_job_id}")
        job_summary = summarize_embedding_job_results(project_id, location, mock_job_id, job_type="batch_prediction")
        print(f"Job Summary: {job_summary}")

        # Example for a custom job (if applicable)
        # mock_custom_job_id = "your-actual-custom-job-id"
        # print(f"\nAttempting to summarize Custom Job ID: {mock_custom_job_id}")
        # custom_job_summary = summarize_embedding_job_results(project_id, location, mock_custom_job_id, job_type="custom_job")
        # print(f"Custom Job Summary: {custom_job_summary}")