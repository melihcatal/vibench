import os

# Load environment variables for the NoSQL service


def get_service_config():
    # Example placeholders – replace with actual defaults if needed
    return {
        "service": os.getenv("NOSQL_SERVICE", "mongodb"),
        "uri": os.getenv("NOSQL_URI"),
        "endpoint": os.getenv("NOSQL_ENDPOINT"),
        "key": os.getenv("NOSQL_KEY"),
        "project_id": os.getenv("NOSQL_PROJECT_ID"),
    }


config = get_service_config()


def get_client():
    """Instantiate and return a client for the selected NoSQL service based on env vars."""
    service = config.get("service", "mongodb").lower()
    if service == "mongodb":
        from pymongo import MongoClient

        uri = config.get("uri")
        return MongoClient(uri)
    elif service == "dynamodb":
        import boto3

        return boto3.resource(
            "dynamodb",
            aws_access_key_id=config.get("key"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
        )
    elif service == "firestore":
        from google.cloud import firestore

        return firestore.Client()
    else:
        raise NotImplementedError(f"Unsupported NoSQL service: {service}")


client = get_client()
