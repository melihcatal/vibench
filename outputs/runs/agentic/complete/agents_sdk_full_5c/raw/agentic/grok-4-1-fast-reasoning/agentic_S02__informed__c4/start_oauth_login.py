&quot;&quot;&quot;
Starts an OAuth or OIDC authorization-code login with Auth0.
&quot;&quot;&quot;
import webbrowser
from typing import Optional
from identity_client import build_authorize_url

def start_oauth_login(
    redirect_uri: str,
    state: Optional[str] = None
) -&gt; str:
    &quot;&quot;&quot;
    Generates and optionally opens the authorization URL.
    &quot;&quot;&quot;
    auth_url = build_authorize_url(redirect_uri, state=state)
    # webbrowser.open(auth_url)  # uncomment to auto-open
    return auth_url