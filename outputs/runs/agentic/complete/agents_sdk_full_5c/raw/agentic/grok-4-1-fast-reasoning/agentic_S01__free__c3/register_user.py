from identity_client import get_supabase_client

def register_user(email: str, password: str):
    supabase = get_supabase_client()
    response = supabase.auth.sign_up({'email': email, 'password': password})
    return {
        'user_id': response.user.id if response.user else None,
        'session': response.session.model_dump() if response.session else None
    }