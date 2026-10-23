import json
import urllib.error
import urllib.parse
import urllib.request

from identity_client import auth_endpoint, auth_params, build_headers
from identity_models import AccountInput, LifecycleResponse


def register_user(email: str, password: str, locale: str = "en", display_name: str = None):
    account = AccountInput(email=email, password=password, locale=locale, display_name=display_name).normalized()
    url = f"{auth_endpoint('accounts:signUp')}?{urllib.parse.urlencode(auth_params())}" if auth_params() else auth_endpoint('accounts:signUp')
    body = {"email": account.email, "password": account.password, "returnSecureToken": True}
    if account.display_name:
        body["displayName"] = account.display_name
    request = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=build_headers(), method="POST")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
            return LifecycleResponse(ok=True, data=data)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8")
        return LifecycleResponse(ok=False, error=detail)
