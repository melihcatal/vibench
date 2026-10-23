import boto3

def summarize_onboarding_state(user_id):
    client = boto3.client('cognito-idp', region_name='us-east-1')
    try:
        response = client.admin_get_user(
            UserPoolId='us-east-1_example',
            Username=user_id
        )
        return response
    except client.exceptions.UserNotFoundException:
        return {'message': 'User not found'}
    except Exception as e:
        return {'error': str(e)}