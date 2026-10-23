&quot;&quot;&quot;
Fetches and normalizes federated user profile claims from Auth0.
&quot;&quot;&quot;
from typing import Dict, Any
from identity_client import fetch_userinfo

def get_profile_claims(access_token: str) -&gt; Dict[str, Any]:
    &quot;&quot;&quot;
    Fetches normalized user profile.
    &quot;&quot;&quot;
    return fetch_userinfo(access_token)