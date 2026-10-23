import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Configuration
AWS_REGION = os.getenv('AWS_REGION', 'us-west-2')

# Client
textract_client = boto3.client('textract', region_name=AWS_REGION)

def configure_textract_client(region=None):
    global textract_client
    if region:
        textract_client = boto3.client('textract', region_name=region)
    else:
        textract_client = boto3.client('textract')

def check_aws_credentials():
    try:
        boto3.client('sts').get_caller_identity()
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise Exception('AWS credentials not configured: ' + str(e))

# Helper Utilities
def start_document_analysis(document_location, feature_types=['FORMS', 'TABLES']):
    response = textract_client.start_document_analysis(
        DocumentLocation=document_location,
        FeatureTypes=feature_types
    )
    return response

def get_document_analysis_result(job_id):
    response = textract_client.get_document_analysis(JobId=job_id)
    return response
