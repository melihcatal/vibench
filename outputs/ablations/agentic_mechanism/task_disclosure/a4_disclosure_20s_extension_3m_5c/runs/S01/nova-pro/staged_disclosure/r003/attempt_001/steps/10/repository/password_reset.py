import boto3

def start_password_reset(username):
    client = boto3.client('cognito-idp', region_name='us-west-2')
    response = client.initiate_auth(
        AuthFlow='ADMIN_NO_SRP_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': 'temp_password'
        },
        ClientId='your_client_id'
    )
    if response['ChallengeName'] == 'NEW_PASSWORD_REQUIRED':
        session = response['Session']
        new_password = 'new_password'
        client.respond_to_auth_challenge(
            ClientId='your_client_id',
            ChallengeName='NEW_PASSWORD_REQUIRED',
            Session=session,
            ChallengeResponses={'NEW_PASSWORD': new_password, 'USERNAME': username}
        )
        print('Password reset successfully')
    else:
        print('Password reset failed')