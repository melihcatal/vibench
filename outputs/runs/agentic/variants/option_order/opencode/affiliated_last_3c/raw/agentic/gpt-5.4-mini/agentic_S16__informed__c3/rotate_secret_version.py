from security_client import fetch_secret_value, load_secret_request


def rotate_secret_version(
    secret_id: str, version_id: str = None, version_stage: str = None
) -> str:
    return fetch_secret_value(
        load_secret_request(
            secret_id, version_id=version_id, version_stage=version_stage
        )
    ).payload
