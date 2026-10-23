from google_auth_oauthlib.flow import InstalledAppFlow


def start_oauth_login():
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/userinfo.profile',
                'https://www.googleapis.com/auth/userinfo.email'])
    flow.run_local_server(port=0)


if __name__ == '__main__':
    start_oauth_login()