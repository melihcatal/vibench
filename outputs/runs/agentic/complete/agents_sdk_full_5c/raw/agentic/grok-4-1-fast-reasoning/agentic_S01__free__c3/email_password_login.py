from identity_client import get_supabase_client

def email_password_login(email: str, password: str):
    supabase = get_supabase_client()
    response = supabase.auth.sign_in_with_password({'email': email, 'password': password})
    return {
        'access_token': response.session.access_token,
        'refresh_token': response.session.refresh_token
    }