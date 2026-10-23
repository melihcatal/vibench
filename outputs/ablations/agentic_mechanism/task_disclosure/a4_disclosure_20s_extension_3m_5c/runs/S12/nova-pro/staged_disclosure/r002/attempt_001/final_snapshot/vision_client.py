import boto3

# Configuration for Amazon Rekognition
AWS_REGION = 'us-west-2'

# Create a low-level service client
def create_rekognition_client():
    return boto3.client('rekognition', region_name=AWS_REGION)

# Example usage
if __name__ == '__main__':
    client = create_rekognition_client()
    print(client)