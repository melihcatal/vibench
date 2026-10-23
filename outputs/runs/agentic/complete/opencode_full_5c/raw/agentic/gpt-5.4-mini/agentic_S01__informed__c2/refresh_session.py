from identity_client import auth0_domain, auth0_request
from identity_models import AccountRequest, AccountResponse


def refresh_session(request: AccountRequest) -> AccountResponse:
    response = auth0_request(
        "POST",
        "/oauth/token",
        json={
            "grant_type": "refresh_token",
            "refresh_token": request.password,
            "client_id": auth0_domain(),
        },
    )
    data = response.json() if response.content else {}
    return AccountResponse(
        ok=response.ok,
        data=data,
        error=None
        if response.ok
        else data.get("error_description", data.get("message", "refresh_failed")),
    )
