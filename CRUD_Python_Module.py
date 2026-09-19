# Example Python Code to Insert a Document 

from pymongo import MongoClient
from bson.objectid import ObjectId


class AnimalShelter(object):
    """ CRUD operations for the Animal collection in MongoDB """

    def __init__(self, username, password):
        # Connection variables -- username/password come in from
        # whoever instantiates this class, so the same code works
        # for any aacuser credentials, not just one hardcoded pair.
        USER = username
        PASS = password
        HOST = 'localhost'
        PORT = 27017
        DB = 'aac'
        COL = 'animals'

        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER, PASS, HOST, PORT))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]

    def create(self, data):
        # data must be a real, non-empty dictionary -- insert_one()
        # expects key/value pairs, and an empty insert isn't useful.
        if data is not None and isinstance(data, dict) and len(data) > 0:
            try:
                result = self.database.animals.insert_one(data)
                # acknowledged confirms MongoDB actually committed the
                # write, not just that insert_one() didn't throw.
                return result.acknowledged
            except Exception as e:
                print("Insert failed:", e)
                return False
        else:
            raise Exception("Nothing to save, because data parameter is empty")

    def read(self, query):
        # find() -- not find_one() -- so a query matching more than
        # one document doesn't silently drop the rest.
        if query is not None and isinstance(query, dict):
            try:
                cursor = self.database.animals.find(query)
                # find() returns a Cursor, a lazy pointer to results
                # still sitting on the server; list() walks it and
                # pulls every matching document into memory.
                return list(cursor)
            except Exception as e:
                print("Query failed:", e)
                return []
        else:
            raise Exception("Nothing to search for, because query parameter is empty")