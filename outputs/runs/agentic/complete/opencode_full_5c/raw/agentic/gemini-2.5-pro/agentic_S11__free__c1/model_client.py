import os
import vertexai


def create_client(project: str, location: str):
    if not project or not location:
        raise ValueError("Google Cloud project and location must be specified.")

    vertexai.init(project=project, location=location)


def get_google_credentials():
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise EnvironmentError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable not set."
        )
    return credentials_path
