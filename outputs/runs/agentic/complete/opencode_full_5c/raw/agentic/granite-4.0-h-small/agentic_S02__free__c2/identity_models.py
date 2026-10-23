import json

class IdentityModels:
    @staticmethod
def load_env_config(env_prefix='AUTH0_'):
        load_dotenv()
        cfg = {}
        for key, val in os.environ.items():
            if key.startswith(env_prefix):
                cfg[key[len(env_prefix):].lower()] = val
        return cfg

    @staticmethod
def normalize_token_response(resp):
        # Convert token response to consistent dict format
        if isinstance(resp, dict):
            return resp
        try:
            return json.loads(resp)
        except Exception:
            raise ValueError("Failed to parse token response")

    @staticmethod
def normalize_profile(claims):
        # Remap common OIDC claims to internal format
        normalized = {
            'user_id': claims.get('sub'),
            'email': claims.get('email'),
            'email_verified': claims.get('email_verified'),
            'given_name': claims.get('given_name'),
            'family_name': claims.get('family_name'),
            'nickname': claims.get('nickname'),
            'locale': claims.get('locale'),
            'picture': claims.get('picture'),
        }
        return normalized
