import boto3

cognito_client = boto3.client('cognito-idp')

def get_onboarding_summary(user_id):
    try:
        response = cognito_client.admin_get_user(
            UserPoolId='your-user-pool-id',
            Username=user_id
        )
        return response
    except Exception as e:
        return str(e)