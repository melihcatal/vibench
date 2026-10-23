import identity_client

def start_google_oauth_login():
    auth_url = identity_client.get_google_auth_url()
    print(f"Redirecting to: {auth_url}")
    # In a real web application, you would redirect the user's browser to this URL.
    # For this example, we'll just print it.
    return auth_url

if __name__ == "__main__":
    start_google_oauth_login()
