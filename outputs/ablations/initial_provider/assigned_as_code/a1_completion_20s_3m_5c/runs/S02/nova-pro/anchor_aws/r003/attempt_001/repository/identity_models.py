from typing import Dict


class IdentityModels:
    @staticmethod
    def normalize_profile(profile: Dict) -> Dict:
        normalized_profile = {}
        for attr in profile:
            if attr['Name'] == 'email':
                normalized_profile['email'] = attr['Value']
            elif attr['Name'] == 'name':
                normalized_profile['name'] = attr['Value']
            elif attr['Name'] == 'sub':
                normalized_profile['sub'] = attr['Value']
        return normalized_profile