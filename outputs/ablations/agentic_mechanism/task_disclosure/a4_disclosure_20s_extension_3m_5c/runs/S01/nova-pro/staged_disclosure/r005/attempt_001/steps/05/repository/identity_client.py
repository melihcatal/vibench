import boto3

# Initialize a Cognito client
cognito_client = boto3.client('cognito-idp')

# Function to sign up a new user
def sign_up(username, password, user_pool_id, client_id):
    try:
        response = cognito_client.sign_up(
            ClientId=client_id,
            Username=username,
            Password=password,
        )
        print('User signed up successfully:', response)
    except Exception as e:
        print('Error signing up:', e)

# Function to confirm a user's account
def confirm_sign_up(username, confirmation_code, client_id):
    try:
        response = cognito_client.confirm_sign_up(
            ClientId=client_id,
            Username=username,
            ConfirmationCode=confirmation_code,
        )
        print('User account confirmed successfully:', response)
    except Exception as e:
        print('Error confirming sign up:', e)

# Function to authenticate a user
def authenticate(username, password, client_id):
    try:
        response = cognito_client.initiate_auth(
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password,
            }
        )
        print('User authenticated successfully:', response)
    except Exception as e:
        print('Error authenticating:', e)