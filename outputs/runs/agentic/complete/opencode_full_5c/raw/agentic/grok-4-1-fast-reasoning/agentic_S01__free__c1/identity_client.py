import os
import stytch


def get_stytch_client():
    return stytch.Client(
        project_id=os.getenv("STYTCH_PROJECT_ID"),
        secret=os.getenv("STYTCH_SECRET"),
    )
