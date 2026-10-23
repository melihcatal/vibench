
import boto3

def get_secret_rotation_summary():
    """
    Summarizes the rotation status of secrets in AWS Secrets Manager.
    """
    secretsmanager_client = boto3.client('secretsmanager')
    
    try:
        response = secretsmanager_client.list_secrets()
        
        print("Secret Rotation Summary:")
        print("------------------------")
        
        for secret in response.get('SecretList', []):
            secret_name = secret.get('Name')
            rotation_enabled = secret.get('RotationEnabled', False)
            last_rotated_date = secret.get('LastRotatedDate')
            
            status = "Enabled" if rotation_enabled else "Disabled"
            last_rotated = last_rotated_date.strftime("%Y-%m-%d %H:%M:%S") if last_rotated_date else "N/A"
            
            print(f"Secret: {secret_name}")
            print(f"  Rotation Status: {status}")
            print(f"  Last Rotated: {last_rotated}")
            print("------------------------")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_secret_rotation_summary()
