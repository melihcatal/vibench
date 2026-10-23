from typing import Dict
# Mock translation map for consent UI strings from major providers
cONSENT_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    'auth0': {
        'en': 'I consent to sharing my profile data with this application.',
        'es': 'Consiento compartir mis datos de perfil con esta aplicación.',
        'fr': 'Je consens à partager mes données de profil avec cette application.',
    },
    'google': {
        'en': 'Allow this app to access your basic profile info?',
        'es': '¿Permitir que esta app acceda a tu información básica de perfil?',
        'fr': 'Étes-vous désirez-vous autoriser cette application à accéder à vos informations de profil?',
    },
    'azure_ad_b2c': {
        'en': 'Do you consent to the requested permissions?',
        'es': '¿Acepta usted los permisos solicitados?',
        'fr': 'Êtes-vous désirez-vous consentir aux autorisations demandées?',
    }
}

def translate_consent(provider: str, locale: str = 'en') -> Optional[str]:
    '''Return a translated consent message for the given provider and locale.'''
    try:
        return conSENT_TRANSLATIONS[provider.lower()][locale]
    except KeyError:
        # Fallback to English if missing
        return conSENT_TRANSLATIONS[provider.lower()]['en']

if __name__ == '__main__':
    print('Auth0 consent (EN):', translate_consent('auth0', 'en'))
    print('Google consent (FR):', translate_consent('google', 'fr'))
    print('Azure consent (ES):', translate_consent('azure_ad_b2c', 'es'))
