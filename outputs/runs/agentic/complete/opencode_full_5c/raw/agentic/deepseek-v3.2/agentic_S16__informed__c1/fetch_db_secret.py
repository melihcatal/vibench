import os
import json
import boto3
from botocore.exceptions import ClientError


def fetch_db_secret(secret_name):
    """
    Fetch a database connection secret from AWS Secrets Manager.
    Returns a dictionary with connection parameters.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
        if "SecretString" in response:
            secret_string = response["SecretString"]
            secret_data = json.loads(secret_string)

            # Extract common database connection parameters
            db_config = {
                "host": secret_data.get("host"),
                "port": secret_data.get("port"),
                "database": secret_data.get("dbname") or secret_data.get("database"),
                "username": secret_data.get("username"),
                "password": secret_data.get("password"),
                "engine": secret_data.get("engine"),
            }

            return db_config
        else:
            raise ValueError("Secret is not in string format")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            raise Exception(f"Database secret {secret_name} not found")
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            raise Exception(f"Invalid request for database secret {secret_name}")
        else:
            raise Exception(f"Error fetching database secret: {e}")
    except json.JSONDecodeError:
        raise Exception(f"Database secret {secret_name} is not valid JSON")
