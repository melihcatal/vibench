import os

IBM_APPID_CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
IBM_APPID_CLIENT_SECRET = os.getenv("IBM_APPID_CLIENT_SECRET")


class IdentityClient:
    def __init__(self):
        self.client_id = IBM_APPID_CLIENT_ID
        self.client_secret = IBM_APPID_CLIENT_SECRET

    def get_auth_header(self):
        return (
            "Basic "
            + base64.b64encode(
                f"{self.client_id}:{self.client_secret}".encode()
            ).decode()
        )
