import os
import json
from dotenv import load_dotenv

load_dotenv()

# AWS Secrets Manager
import boto3

client = boto3.client("secretsmanager")


def fetch_api_key():
    # Retrieve API key secret named 'my-api-key'
    response = client.get_secret_value(SecretId="my-api-key")
    secret = json.loads(response["SecretString"])
    return secret["key"]


def fetch_db_secret():
    # Retrieve database secret named 'my-db-secret'
    response = client.get_secret_value(SecretId="my-db-secret")
    secret = json.loads(response["SecretString"])
    return secret
