from identity_client import auth0_request, normalized_payload
from identity_models import AccountRequest, AccountResponse


def password_reset(request: AccountRequest) -> AccountResponse:
    response = auth0_request(
        "POST",
        "/dbconnections/change_password",
        json=normalized_payload(
            request.email,
            request.locale,
            client_id="AUTH0_CLIENT_ID",
            connection="Username-Password-Authentication",
        ),
    )
    data = response.json() if response.content else {}
    return AccountResponse(
        ok=response.ok,
        data=data,
        error=None if response.ok else data.get("message", "reset_failed"),
    )
