&quot;&quot;&quot;
Handles the OAuth callback and exchanges authorization code for tokens with Auth0.
&quot;&quot;&quot;
import os
from typing import Optional, Dict, Any
from identity_client import exchange_authorization_code

def handle_oauth_callback(
    code: str,
    redirect_uri: str,
    client_secret: Optional[str] = None
) -&gt; Dict[str, Any]:
    &quot;&quot;&quot;
    Exchanges the authorization code for tokens.
    &quot;&quot;&quot;
    if client_secret is None:
        client_secret = os.getenv(&#x27;AUTH0_CLIENT_SECRET&#x27;)
    tokens = exchange_authorization_code(code, redirect_uri, client_secret=client_secret)
    return tokens