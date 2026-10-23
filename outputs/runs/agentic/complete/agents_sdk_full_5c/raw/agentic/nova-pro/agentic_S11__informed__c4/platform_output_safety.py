TISANE_API_KEY')}'},
        json={'text': text}
    )
    return response.json()['is_safe']