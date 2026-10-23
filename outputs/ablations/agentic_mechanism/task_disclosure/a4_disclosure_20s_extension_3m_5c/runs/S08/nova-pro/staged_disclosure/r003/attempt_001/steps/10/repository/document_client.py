import boto3

# Configuration
AWS_REGION = 'us-west-2'

# Client Helper
def get_textract_client():
    return boto3.client('textract', region_name=AWS_REGION)

# Example usage
if __name__ == '__main__':
    textract_client = get_textract_client()
    print(textract_client)