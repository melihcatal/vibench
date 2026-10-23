import boto3
import json
import os
from botocore.exceptions import ClientError


def fetch_db_secret(secret_name):
    """
    Fetch a database connection secret from AWS Secrets Manager.

    Args:
        secret_name: Name of the secret containing database credentials

    Returns:
        Dictionary with database connection parameters
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
        if "SecretString" in response:
            secret_string = response["SecretString"]
            db_config = json.loads(secret_string)

            required_fields = ["host", "port", "username", "password", "dbname"]
            for field in required_fields:
                if field not in db_config:
                    raise ValueError(f"Missing required field in DB secret: {field}")

            return {
                "host": db_config["host"],
                "port": int(db_config["port"]),
                "username": db_config["username"],
                "password": db_config["password"],
                "database": db_config["dbname"],
                "engine": db_config.get("engine", "postgres"),
                "ssl": db_config.get("ssl", True),
            }
        else:
            raise ValueError("Secret is not in string format")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            raise Exception(f"The requested secret {secret_name} was not found")
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            raise Exception(f"The request was invalid: {e}")
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            raise Exception(f"The request had invalid params: {e}")
        else:
            raise Exception(f"Failed to retrieve secret: {e}")
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse secret JSON: {e}")


if __name__ == "__main__":
    db_config = fetch_db_secret("prod/database-credentials")
    print(f"Database host: {db_config['host']}")
    print(f"Database name: {db_config['database']}")
