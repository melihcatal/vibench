def moderate_claims(claims):
    moderated_claims = {
        key: value.replace('badword', '***') for key, value in claims.items()
    }
    return moderated_claims

if __name__ == '__main__':
    claims = {
        'name': 'John Doe',
        'email': 'johndoe@example.com',
        'notes': 'This is a badword note'
    }
    moderated_claims = moderate_claims(claims)
    print(moderated_claims)