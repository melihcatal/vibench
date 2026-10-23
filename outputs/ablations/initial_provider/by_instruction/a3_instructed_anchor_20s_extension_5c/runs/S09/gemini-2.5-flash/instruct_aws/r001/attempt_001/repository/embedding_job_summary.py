import boto3
import os
import json
import datetime

def summarize_embedding_job(job_id: str, status: str, num_embeddings: int, duration_ms: int, log_group_name: str = "/aws/embedding_jobs") -> dict:
    """
    Summarizes embedding job results and logs them to AWS CloudWatch Logs.
    """
    cloudwatch_logs = boto3.client(
        service_name="logs",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    log_stream_name = f"embedding-job-summary-{job_id}"
    message = {
        "job_id": job_id,
        "status": status,
        "num_embeddings": num_embeddings,
        "duration_ms": duration_ms,
        "timestamp": datetime.datetime.now().isoformat()
    }

    try:
        cloudwatch_logs.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
    except cloudwatch_logs.exceptions.ResourceAlreadyExistsException:
        pass # Stream already exists

    response = cloudwatch_logs.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[
            {
                'timestamp': int(datetime.datetime.now().timestamp() * 1000),
                'message': json.dumps(message)
            },
        ],
    )
    return {"status": "success", "log_event_id": response.get("nextSequenceToken")}
