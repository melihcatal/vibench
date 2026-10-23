import os
import boto3


class IdentityClient:
    def __init__(self, config):
        self.config = config
        self.cognito_client = boto3.client('cognito-idp', region_name=config['region'])
        self.domain = f"https://{config['domain_prefix']}.auth.{config['region']}.amazoncognito.com"

    def exchange_code_for_tokens(self, code, redirect_uri):
        response = self.cognito_client.initiate_auth(
            AuthFlow='CODE',
            AuthParameters={'code': code, 'redirect_uri': redirect_uri},
            ClientId=self.config['client_id']
        )
        return response['AuthenticationResult']

    def get_profile(self, id_token):
        response = self.cognito_client.get_user(
            AccessToken=id_token
        )
        return response['UserAttributes']

    def get_authorization_url(self, query):
        query_string = urlencode(query)
        return f"{self.domain}/oauth2/authorize?{query_string}"