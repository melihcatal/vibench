import identity_client

def start_login():
    """Constructs and prints the Azure AD authorization URL."""
    auth_url = identity_client.build_auth_url(scopes=identity_client.AZURE_AD_SCOPES)
    print(f"Please visit this URL to log in: {auth_url}")
    return auth_url

if __name__ == "__main__":
    start_login()
