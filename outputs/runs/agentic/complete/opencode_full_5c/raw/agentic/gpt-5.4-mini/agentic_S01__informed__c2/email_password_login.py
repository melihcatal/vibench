from identity_client import auth0_domain, auth0_request, normalized_payload
from identity_models import AccountRequest, AccountResponse


def email_password_login(request: AccountRequest) -> AccountResponse:
    payload = normalized_payload(
        request.email,
        request.locale,
        grant_type="password",
        username=request.email,
        password=request.password,
        audience=f"https://{auth0_domain()}/api/v2/",
        scope="openid profile email",
    )
    response = auth0_request("POST", "/oauth/token", json=payload)
    data = response.json() if response.content else {}
    return AccountResponse(
        ok=response.ok,
        data=data,
        error=None
        if response.ok
        else data.get("error_description", data.get("message", "login_failed")),
    )
