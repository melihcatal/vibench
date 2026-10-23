import boto3

def check_platform_output_safety(output):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(TextSegments=[output])
    return response