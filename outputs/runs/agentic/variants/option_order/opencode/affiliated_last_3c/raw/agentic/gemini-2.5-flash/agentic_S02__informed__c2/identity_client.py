import os


def get_auth0_domain():
    return os.environ.get("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN.auth0.com")


def get_auth0_client_id():
    return os.environ.get("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID")


def get_auth0_client_secret():
    return os.environ.get("AUTH0_CLIENT_SECRET", "YOUR_AUTH0_CLIENT_SECRET")


def get_google_api_key():
    return os.environ.get("GOOGLE_API_KEY", "YOUR_GOOGLE_API_KEY")


def get_perspective_api_key():
    return os.environ.get("PERSPECTIVE_API_KEY", "YOUR_PERSPECTIVE_API_KEY")


def get_google_application_credentials():
    # For Google Cloud services, GOOGLE_APPLICATION_CREDENTIALS points to a JSON key file
    return os.environ.get(
        "GOOGLE_APPLICATION_CREDENTIALS", "/path/to/your/google-credentials.json"
    )


def get_google_cloud_project():
    return os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
