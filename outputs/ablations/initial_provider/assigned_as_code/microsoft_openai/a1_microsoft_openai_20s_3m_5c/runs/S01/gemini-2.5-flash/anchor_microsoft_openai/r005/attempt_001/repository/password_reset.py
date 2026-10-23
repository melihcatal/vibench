from identity_client import AzureADB2CClient
from identity_models import PasswordResetRequest

def password_reset(request: PasswordResetRequest):
    client = AzureADB2CClient()
    # In Azure AD B2C, password reset is typically a user-initiated flow
    # where the user is redirected to a B2C policy endpoint.
    # This function returns the URL to redirect the user to.
    reset_url_info = client.initiate_password_reset(request.email)
    return reset_url_info
