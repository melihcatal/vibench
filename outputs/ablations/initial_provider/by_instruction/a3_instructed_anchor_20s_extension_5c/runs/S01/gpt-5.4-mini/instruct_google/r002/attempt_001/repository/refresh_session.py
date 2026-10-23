import json
import urllib.error
import urllib.parse
import urllib.request

from identity_client import auth_endpoint, auth_params, build_headers
from identity_models import LifecycleResponse


def refresh_session(refresh_token: str):
    query = urllib.parse.urlencode(auth_params())
    url = f"{auth_endpoint('token')}?{query}" if query else auth_endpoint('token')
    payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}
    request = urllib.request.Request(url, data=urllib.parse.urlencode(payload).encode("utf-8"), headers=build_headers(), method="POST")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
            return LifecycleResponse(ok=True, data=data)
    except urllib.error.HTTPError as exc:
        return LifecycleResponse(ok=False, error=exc.read().decode("utf-8"))
