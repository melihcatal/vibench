import os
import boto3


def get_cognito_client():
    aws_region = os.environ.get("AWS_REGION", "us-east-1")  # Example default region
    return boto3.client("cognito-idp", region_name=aws_region)


def get_cognito_user_pool_id():
    user_pool_id = os.environ.get("COGNITO_USER_POOL_ID")
    if not user_pool_id:
        raise ValueError("COGNITO_USER_POOL_ID environment variable not set")
    return user_pool_id


def get_cognito_client_id():
    client_id = os.environ.get("COGNITO_CLIENT_ID")
    if not client_id:
        raise ValueError("COGNITO_CLIENT_ID environment variable not set")
    return client_id


def get_google_cloud_project_id():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set")
    return project_id


def get_mongodb_connection_string():
    conn_string = os.environ.get("MONGODB_CONNECTION_STRING")
    if not conn_string:
        raise ValueError("MONGODB_CONNECTION_STRING environment variable not set")
    return conn_string


def get_mongodb_database_name():
    db_name = os.environ.get("MONGODB_DATABASE_NAME", "onboarding_db")
    return db_name


def get_mongodb_collection_name():
    collection_name = os.environ.get("MONGODB_COLLECTION_NAME", "profile_notes")
    return collection_name
