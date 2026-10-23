class IdentityModels:
    @staticmethod
    def normalize_user(user):
        return {
            'user_id': user['user_id'],
            'email': user['email'],
            'created_at': user['created_at']
        }