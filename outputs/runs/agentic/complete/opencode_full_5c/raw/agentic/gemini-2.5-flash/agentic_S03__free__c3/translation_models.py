import os

# Define constants for project and location, potentially from environment variables
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "global")

# In a more complex scenario, this file would contain Pydantic models or dataclasses
# for request/response bodies, but for direct SDK usage, simple functions suffice.


def get_project_id():
    return PROJECT_ID


def get_location():
    return LOCATION
