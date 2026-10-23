import boto3
from botocore.exceptions import NoCredentialsError

DOCUMENTDB_CLUSTER_ARN = 'arn:aws:rds:us-west-2:123456789012:cluster:my-documentdb-cluster'
DOCUMENTDB_SECRET_ARN = 'arn:aws:secretsmanager:us-west-2:123456789012:secret:my-documentdb-secret'

def store_audit_record(record):
    try:
        client = boto3.client('rds-data')
        response = client.execute_statement(
            resourceArn=DOCUMENTDB_CLUSTER_ARN,
            secretArn=DOCUMENTDB_SECRET_ARN,
            database='auditdb',
            sql='INSERT INTO audit_records VALUES (:record)',
            parameters=[
                {
                    'name': 'record',
                    'value': {
                        'stringValue': str(record)
                    }
                }
            ]
        )
        print('Audit record stored successfully')
    except NoCredentialsError:
        print('Credentials not available')

# Example usage
audit_record = {
    'user_id': 'user123',
    'login_time': '2026-09-20T12:34:56Z',
    'ip_address': '192.168.1.1'
}
store_audit_record(audit_record)