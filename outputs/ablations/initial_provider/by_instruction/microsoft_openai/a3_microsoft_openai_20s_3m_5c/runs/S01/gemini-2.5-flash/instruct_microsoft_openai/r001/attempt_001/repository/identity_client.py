import os

class IdentityClientConfig:
    def __init__(self):
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.firebase_service_account_key_path = os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY_PATH")
        self.aws_region = os.environ.get("AWS_REGION")
        self.sendgrid_api_key = os.environ.get("SENDGRID_API_KEY")
        # Add any other common configuration parameters here

    def get_openai_api_key(self):
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set in IdentityClientConfig.")
        return self.openai_api_key

    def get_firebase_service_account_key_path(self):
        if not self.firebase_service_account_key_path:
            raise ValueError("FIREBASE_SERVICE_ACCOUNT_KEY_PATH environment variable not set in IdentityClientConfig.")
        return self.firebase_service_account_key_path

    def get_aws_region(self):
        if not self.aws_region:
            raise ValueError("AWS_REGION environment variable not set in IdentityClientConfig.")
        return self.aws_region

    def get_sendgrid_api_key(self):
        if not self.sendgrid_api_key:
            raise ValueError("SENDGRID_API_KEY environment variable not set in IdentityClientConfig.")
        return self.sendgrid_api_key

class IdentityClient:
    def __init__(self, config: IdentityClientConfig):
        self.config = config

    # This client could potentially hold initialized SDK clients for various providers
    # For instance, an initialized firebase_admin app or boto3 client.
    # For now, it just holds the config.
