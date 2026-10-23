import boto3

def summarize_secret_rotation_status():
    client = boto3.client('''secretsmanager''')

    paginator = client.get_paginator('''list_secrets''')
    response_iterator = paginator.paginate()

    rotation_summary = []

    for page in response_iterator:
        for secret in page['''SecretList''']:
            secret_arn = secret['''ARN''']
            secret_name = secret['''Name''']
            
            try:
                description_response = client.describe_secret(SecretId=secret_arn)
                rotation_enabled = description_response.get('''RotationEnabled''', False)
                rotation_lambda_arn = description_response.get('''RotationLambdaARN''')
                last_rotated_date = description_response.get('''LastRotatedDate''')
                next_rotation_date = description_response.get('''NextRotationDate''')

                summary_item = {
                    '''SecretName''': secret_name,
                    '''RotationEnabled''': rotation_enabled,
                    '''RotationLambdaARN''': rotation_lambda_arn,
                    '''LastRotatedDate''': last_rotated_date,
                    '''NextRotationDate''': next_rotation_date
                }
                rotation_summary.append(summary_item)
            except Exception as e:
                rotation_summary.append({
                    '''SecretName''': secret_name,
                    '''Error''': str(e)
                })
    
    return rotation_summary

if __name__ == '''__main__''':
    summary = summarize_secret_rotation_status()
    import json
    print(json.dumps(summary, indent=4, default=str))
