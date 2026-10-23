import json
import urllib.error
import urllib.parse
import urllib.request

from identity_client import auth_endpoint, auth_params, build_headers, parse_json_response
from identity_models import AccountInput, LifecycleResponse


def email_password_login(email: str, password: str):
    account = AccountInput(email=email, password=password).normalized()
    query = urllib.parse.urlencode(auth_params())
    url = f"{auth_endpoint('accounts:signInWithPassword')}?{query}" if query else auth_endpoint('accounts:signInWithPassword')
    payload = {"email": account.email, "password": account.password, "returnSecureToken": True}
    request = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=build_headers(), method="POST")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = parse_json_response(json.loads(response.read().decode("utf-8")))
            return LifecycleResponse(ok=True, data=data)
    except urllib.error.HTTPError as exc:
        return LifecycleResponse(ok=False, error=exc.read().decode("utf-8"))
