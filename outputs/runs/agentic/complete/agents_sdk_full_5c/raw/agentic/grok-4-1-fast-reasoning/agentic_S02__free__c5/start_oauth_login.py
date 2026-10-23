import webbrowser
from identity_client import Auth0Client

def start_oauth_login():
    client = Auth0Client()
    authorize_url = client.get_authorize_url()
    print(f"Opening Auth0 OAuth login: {authorize_url}")
    webbrowser.open(authorize_url)

if __name__ == "__main__":
    start_oauth_login()