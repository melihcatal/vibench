&quot;&quot;&quot;
Implements a PKCE login flow for public clients with Auth0.
&quot;&quot;&quot;
from typing import Optional, Tuple, Dict, Any
from identity_client import generate_pkce_pair, build_authorize_url, exchange_authorization_code

def start_pkce_login(
    redirect_uri: str,
    state: Optional[str] = None
) -&gt; Tuple[str, str]:
    &quot;&quot;&quot;
    Starts PKCE flow, returns (auth_url, code_verifier).
    Store verifier securely for exchange.
    &quot;&quot;&quot;
    verifier, challenge = generate_pkce_pair()
    auth_url = build_authorize_url(
        redirect_uri, state=state, code_challenge=challenge
    )
    return auth_url, verifier

def complete_pkce_login(
    code: str,
    redirect_uri: str,
    verifier: str
) -&gt; Dict[str, Any]:
    &quot;&quot;&quot;
    Completes PKCE flow by exchanging code.
    &quot;&quot;&quot;
    return exchange_authorization_code(code, redirect_uri, code_verifier=verifier)