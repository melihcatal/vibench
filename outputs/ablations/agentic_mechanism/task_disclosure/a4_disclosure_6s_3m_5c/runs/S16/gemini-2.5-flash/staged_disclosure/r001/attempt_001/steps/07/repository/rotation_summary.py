
import boto3

def get_secret_rotation_summary():
    # AWS Secrets Manager client
    client = boto3.client('secretsmanager')

    # List all secrets
    try:
        paginator = client.get_paginator('list_secrets')
        response_iterator = paginator.paginate()
        
        secret_names = []
        for page in response_iterator:
            for secret in page['SecretList']:
                secret_names.append(secret['Name'])
        
        if secret_names:
            summary = "Found the following secrets in AWS Secrets Manager:\n"
            for name in secret_names:
                summary += f"- {name}\n"
            return summary
        else:
            return "No secrets found in AWS Secrets Manager."
            
    except Exception as e:
        return f"Error accessing AWS Secrets Manager: {e}"

if __name__ == "__main__":
    print(get_secret_rotation_summary())
