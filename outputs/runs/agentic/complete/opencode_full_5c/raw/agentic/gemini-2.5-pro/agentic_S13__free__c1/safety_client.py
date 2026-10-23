import os
from googleapiclient import discovery


def get_perspective_client():
    """
    Initializes and returns a Google API client for the Perspective API.
    Requires the 'PERSPECTIVE_API_KEY' environment variable to be set.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    # API client object
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )
    return client
