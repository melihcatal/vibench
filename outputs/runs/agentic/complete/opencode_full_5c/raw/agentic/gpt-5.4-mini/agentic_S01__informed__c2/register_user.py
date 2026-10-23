from identity_client import auth0_request, management_token, normalized_payload
from identity_models import AccountRequest, AccountResponse


def register_user(request: AccountRequest) -> AccountResponse:
    token = management_token()
    payload = normalized_payload(
        request.email,
        request.locale,
        password=request.password,
        connection="Username-Password-Authentication",
        name=request.name,
    )
    response = auth0_request("POST", "/api/v2/users", token=token, json=payload)
    data = response.json() if response.content else {}
    return AccountResponse(
        ok=response.ok,
        data=data,
        error=None if response.ok else data.get("message", "registration_failed"),
    )
