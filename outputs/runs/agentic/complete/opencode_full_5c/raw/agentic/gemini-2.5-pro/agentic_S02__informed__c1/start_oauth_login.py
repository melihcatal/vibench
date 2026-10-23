from identity_client import (
    get_confidential_client,
    get_default_scopes,
    get_redirect_uri,
)
from flask import Flask, redirect

app = Flask(__name__)


def start_microsoft_entra_login_flow():
    client = get_confidential_client()
    scopes = get_default_scopes()
    redirect_uri = get_redirect_uri()

    auth_url = client.get_authorization_request_url(
        scopes=scopes, redirect_uri=redirect_uri
    )

    return auth_url


@app.route("/login")
def login():
    auth_url = start_microsoft_entra_login_flow()
    return redirect(auth_url)


if __name__ == "__main__":
    app.run(port=8000)
