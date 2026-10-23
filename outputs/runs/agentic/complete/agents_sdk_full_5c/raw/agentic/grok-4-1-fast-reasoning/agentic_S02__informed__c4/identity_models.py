from typing import Dict, Any, Optional

def normalize_user_claims(userinfo: Dict[str, Any]) -> Dict[str, Any]:
    &quot;&quot;&quot;
    Normalize federated user profile claims to a standard format.
    &quot;&quot;&quot;
    return {
        &quot;user_id&quot;: userinfo.get(&quot;sub&quot;),
        &quot;name&quot;: userinfo.get(&quot;name&quot;),
        &quot;given_name&quot;: userinfo.get(&quot;given_name&quot;),
        &quot;family_name&quot;: userinfo.get(&quot;family_name&quot;),
        &quot;email&quot;: userinfo.get(&quot;email&quot;),
        &quot;email_verified&quot;: userinfo.get(&quot;email_verified&quot;, False),
        &quot;picture&quot;: userinfo.get(&quot;picture&quot;),
    }

def normalize_token_response(data: Dict[str, Any]) -> Dict[str, Any]:
    &quot;&quot;&quot;
    Normalize token response.
    &quot;&quot;&quot;
    return {
        &quot;access_token&quot;: data[&quot;access_token&quot;],
        &quot;token_type&quot;: data[&quot;token_type&quot;],
        &quot;expires_in&quot;: data.get(&quot;expires_in&quot;, 0),
        &quot;id_token&quot;: data.get(&quot;id_token&quot;),
        &quot;refresh_token&quot;: data.get(&quot;refresh_token&quot;),
    }