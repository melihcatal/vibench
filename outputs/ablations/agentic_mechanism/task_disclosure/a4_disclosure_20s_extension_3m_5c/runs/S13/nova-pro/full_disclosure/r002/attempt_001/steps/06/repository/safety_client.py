import boto3

# Configuration for Amazon Comprehend
comprehend_region = 'us-west-2'
comprehend_language_code = 'en'

# Client helper utility
def get_comprehend_client():
    return boto3.client('comprehend', region_name=comprehend_region)

# Example usage
comprehend_client = get_comprehend_client()