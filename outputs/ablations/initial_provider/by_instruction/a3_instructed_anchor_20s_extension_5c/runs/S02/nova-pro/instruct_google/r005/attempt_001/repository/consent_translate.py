def translate_consent_copy(language):
    translations = {
        'en': 'By continuing, you agree to our Terms of Service and Privacy Policy.',
        'es': 'Al continuar, acepta nuestros Términos de Servicio y Política de Privacidad.',
        'fr': 'En continuant, vous acceptez nos Conditions d’utilisation et notre Politique de confidentialité.'
    }
    return translations.get(language, 'Language not supported')

if __name__ == '__main__':
    language = 'en'
    translated_copy = translate_consent_copy(language)
    print(translated_copy)