from identity_client import get_supabase_client

def refresh_session(refresh_token: str):
    supabase = get_supabase_client()
    response = supabase.auth.refresh_session({'refresh_token': refresh_token})
    return {
        'access_token': response.session.access_token,
        'refresh_token': response.session.refresh_token
    }