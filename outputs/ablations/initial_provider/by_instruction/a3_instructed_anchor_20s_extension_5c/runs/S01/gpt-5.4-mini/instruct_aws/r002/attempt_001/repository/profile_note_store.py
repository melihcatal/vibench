from identity_client import dynamodb_resource


def store_profile_note(user_id: str, note: str, locale: str):
    table = dynamodb_resource().Table(__import__("os").environ["PROFILE_NOTES_TABLE"])
    item = {"user_id": user_id, "note": note, "locale": locale}
    table.put_item(Item=item)
    return item
