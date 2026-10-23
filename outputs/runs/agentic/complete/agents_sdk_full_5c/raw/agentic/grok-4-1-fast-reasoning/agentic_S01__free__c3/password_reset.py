from identity_client import get_supabase_client

def password_reset(email: str):
    supabase = get_supabase_client()
    supabase.auth.reset_password_for_email(email)
    return {'message': 'Password reset email sent'}