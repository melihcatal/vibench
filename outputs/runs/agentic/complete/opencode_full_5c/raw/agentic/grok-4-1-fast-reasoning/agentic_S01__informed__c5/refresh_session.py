from identity_client import cognito_client, APP_CLIENT_ID
from identity_models import RefreshRequest, parse_auth_result


def refresh_session(req: RefreshRequest) -> dict:
    """
    Refreshes an expired session or access token using Amazon Cognito User Pools.
    """
    response = cognito_client.initiate_auth(
        AuthFlow="REFRESH_TOKEN_AUTH",
        ClientId=APP_CLIENT_ID,
        AuthParameters={"REFRESH_TOKEN": req["refresh_token"]},
    )
    return parse_auth_result(response)
