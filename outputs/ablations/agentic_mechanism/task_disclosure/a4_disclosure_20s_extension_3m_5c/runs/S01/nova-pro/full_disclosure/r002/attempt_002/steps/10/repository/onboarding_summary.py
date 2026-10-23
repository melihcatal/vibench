import boto3

def summarize_onboarding_state(user_id):
    client = boto3.client('cognito-idp', region_name='us-east-1')
    try:
        response = client.admin_get_user(
            UserPoolId='us-east-1_ExamplePoolId',
            Username=user_id
        )
        user_attributes = response['UserAttributes']
        summary = {
            'user_id': user_id,
            'email': next((attr['Value'] for attr in user_attributes if attr['Name'] == 'email'), None),
            'phone_number': next((attr['Value'] for attr in user_attributes if attr['Name'] == 'phone_number'), None),
            'enabled': response['Enabled'],
            'user_status': response['UserStatus']
        }
        return summary
    except client.exceptions.UserNotFoundException:
        return {'error': 'User not found'}
    except Exception as e:
        return {'error': str(e)}