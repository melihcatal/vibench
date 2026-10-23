from typing import Dict, Any

def build_user_attributes(email: str, **kwargs: Any) -&gt; list[Dict[str, str]]:
    attrs = [{'Name': 'email', 'Value': email}]
    for name, value in kwargs.items():
        attrs.append({'Name': name, 'Value': str(value)})
    return attrs