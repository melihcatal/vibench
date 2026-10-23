import os
import google.auth
from google.cloud import kms
import boto3
import cohere

def get_kms_client():
    credentials, project = google.auth.default()
    return kms.KeyManagementServiceClient(credentials=credentials)

def get_cloudtrail_client(region_name):
    return boto3.client("cloudtrail", region_name=region_name)

def get_comprehend_client(region_name):
    return boto3.client("comprehend", region_name=region_name)

def get_cohere_client(api_key):
    return cohere.Client(api_key)

def get_translate_client(region_name):
    return boto3.client("translate", region_name=region_name)
