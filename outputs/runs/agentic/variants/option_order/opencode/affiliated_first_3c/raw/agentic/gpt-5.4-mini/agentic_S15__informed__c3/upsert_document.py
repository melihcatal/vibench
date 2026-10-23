from database_client import get_container
from database_models import make_upsert_request


def upsert_document(document, id_field="id"):
    item = make_upsert_request(document, id_field=id_field)
    return get_container().upsert_item(item)
