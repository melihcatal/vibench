import json
import sys

import boto3


def summarize_embedding_job(job_id: str) -> dict[str, object]:
    client = boto3.client("bedrock")
    response = client.get_model_invocation_job(jobIdentifier=job_id)
    return {
        "job_id": job_id,
        "status": response.get("status"),
        "submitted_at": response.get("submittedAt").isoformat() if response.get("submittedAt") else None,
        "ended_at": response.get("endedAt").isoformat() if response.get("endedAt") else None,
        "job_message": response.get("message"),
    }


def main() -> None:
    print(json.dumps(summarize_embedding_job(sys.argv[1])))


if __name__ == "__main__":
    main()
