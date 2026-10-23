import boto3

def summarize_onboarding_state(user_id):
    cognito_client = boto3.client('cognito-idp', region_name='us-west-2')
    try:
        response = cognito_client.admin_get_user(
            UserPoolId='us-west-2_examplePoolId',
            Username=user_id
        )
        user_attributes = response['UserAttributes']
        onboarding_state = {
            'user_id': user_id,
            'email': next((attr['Value'] for attr in user_attributes if attr['Name'] == 'email'), None),
            'phone_number': next((attr['Value'] for attr in user_attributes if attr['Name'] == 'phone_number'), None),
            'enabled': response['Enabled'],
            'user_status': response['UserStatus'],
            'user_create_date': response['UserCreateDate'].isoformat()
        }
        return onboarding_state
    except Exception as e:
        print(f'Error summarizing onboarding state: {e}')
        return None