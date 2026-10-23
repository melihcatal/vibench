import os

import boto3


class IdentityClient:
    def __init__(self):
        self.cognito_client = boto3.client('cognito-idp', region_name=os.getenv('AWS_REGION'))
        self.user_pool_id = os.getenv('COGNITO_USER_POOL_ID')
        self.client_id = os.getenv('COGNITO_CLIENT_ID')

    def initiate_auth(self, email, password):
        try:
            response = self.cognito_client.initiate_auth(
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password
                },
                ClientId=self.client_id
            )
            return response
        except Exception as e:
            print(f'Error during authentication: {e}')
            return None

    def sign_up(self, email, password):
        try:
            response = self.cognito_client.sign_up(
                ClientId=self.client_id,
                Username=email,
                Password=password,
                UserAttributes=[
                    {
                        'Name': 'email',
                        'Value': email
                    }
                ]
            )
            return response
        except Exception as e:
            print(f'Error during sign up: {e}')
            return None

    def confirm_sign_up(self, email, confirmation_code):
        try:
            response = self.cognito_client.confirm_sign_up(
                ClientId=self.client_id,
                Username=email,
                ConfirmationCode=confirmation_code
            )
            return response
        except Exception as e:
            print(f'Error during confirmation: {e}')
            return None

    def forgot_password(self, email):
        try:
            response = self.cognito_client.forgot_password(
                ClientId=self.client_id,
                Username=email
            )
            return response
        except Exception as e:
            print(f'Error during forgot password: {e}')
            return None

    def confirm_forgot_password(self, email, confirmation_code, new_password):
        try:
            response = self.cognito_client.confirm_forgot_password(
                ClientId=self.client_id,
                Username=email,
                ConfirmationCode=confirmation_code,
                Password=new_password
            )
            return response
        except Exception as e:
            print(f'Error during confirm forgot password: {e}')
            return None