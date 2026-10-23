import json
import urllib.error
import urllib.parse
import urllib.request

from identity_client import auth_endpoint, auth_params, build_headers
from identity_models import AccountInput, LifecycleResponse


def password_reset(email: str, locale: str = "en"):
    account = AccountInput(email=email, password="x", locale=locale).normalized()
    query = urllib.parse.urlencode(auth_params())
    url = f"{auth_endpoint('accounts:sendOobCode')}?{query}" if query else auth_endpoint('accounts:sendOobCode')
    payload = {"requestType": "PASSWORD_RESET", "email": account.email, "languageCode": account.locale}
    request = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=build_headers(), method="POST")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return LifecycleResponse(ok=True, data=json.loads(response.read().decode("utf-8")))
    except urllib.error.HTTPError as exc:
        return LifecycleResponse(ok=False, error=exc.read().decode("utf-8"))
