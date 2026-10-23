def parse_signup_response(response):
    return {"user": response.get("user", {}), "session": response.get("session", {})}


def parse_login_response(response):
    return parse_signup_response(response)


def parse_refresh_response(response):
    session = response.get("data", {}).get("session", {})
    return {"session": session}
