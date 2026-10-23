import os

from amazon_nova_sdk import NovaClient


class IdentityClient:
    def __init__(self):
        self.client = NovaClient(
            api_key=os.getenv('NOVA_API_KEY'),
            model_id='amazon-nova-api/nova-pro-v1'
        )

    def federated_login(self, provider, token):
        response = self.client.federated_login(
            provider=provider,
            token=token
        )
        return response
