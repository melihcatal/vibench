# Local helper file: configuration utilities
import os

# Example: load AWS credentials from environment variables (if required)
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# Placeholders for other providers if needed
MINDEE_API_KEY = os.getenv('MINDEE_API_KEY')


def get_client(service_name: str):
    """Return a configured client for the given service.",
    if service_name == 'textract':
        return boto3.client(
            'textract',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name='us-east-1'
        )
    elif service_name == 'mindee':
        import mindee
        return mindee.MindeeClient(MINDEE_API_KEY)
    # Add other providers as necessary
    raise ValueError(f'Unsupported service: {service_name}')
