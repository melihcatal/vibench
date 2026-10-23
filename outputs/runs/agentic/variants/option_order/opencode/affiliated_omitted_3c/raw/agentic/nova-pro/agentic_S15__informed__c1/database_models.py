from database_client import db


class Document:
    def __init__(self, id, data):
        self.id = id
        self.data = data
