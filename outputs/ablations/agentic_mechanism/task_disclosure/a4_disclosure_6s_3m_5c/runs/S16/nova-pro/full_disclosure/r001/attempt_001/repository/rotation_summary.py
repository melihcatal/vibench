import boto3

def summarize_secret_rotation_status(secret_id):
    client = boto3.client('secretsmanager')
    try:
        response = client.describe_secret(SecretId=secret_id)
        versions = client.list_secret_version_ids(SecretId=secret_id)
        current_version = [v for v in versions['Versions'] if v['VersionStages'] == ['AWSCURRENT']][0]
        summary = {
            'SecretId': secret_id,
            'CurrentVersionId': current_version['VersionId'],
            'RotationEnabled': response['RotationEnabled'],
            'RotationLambdaARN': response.get('RotationRules', {}).get('AutomaticallyAfterDays', None),
            'LastRotatedDate': current_version.get('CreatedDate', None)
        }
        return summary
    except client.exceptions.ResourceNotFoundException:
        return {'error': 'Secret not found'}
    except Exception as e:
        return {'error': str(e)}