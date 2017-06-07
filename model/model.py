"""."""
from pymongo import MongoClient
import json


class EntityDoesntExistException(Exception):
    """Exception for an entity that doesn't exists."""

    def __init__(self):
        """Exception initialization."""
        Exception.__init__(self)


class Model(object):
    """Base class for model definition on the framework.

    You must extend this class to define your application model when you need.
    All attributes of the extended class will be automatically saved on the
    database when you save it and retrieved when you find them.

    To save an instance that you have created you could use the 'save' method
    on the instance or the 'save_one' on the class and pass the instance by
    argument.

    To retrieve the database elements you could use the 'find' method on the
    class. TODO: add find arguments to filter.

    To delete an instance you could use the 'delete' method on the instance or
    the 'delete_one' method on the class and pass the instance by argument.
    """

    def save(self):
        """Save or replace the instance on the database.

        Use this method to save a new instance to the database or to update an
        already saved instance.
        """
        mongoClient = MongoClient()
        db = mongoClient['rest_testing']
        collection = db[type(self).__name__]
        if (hasattr(self, '_id')):
            collection.replace_one(
                {'_id': self._id},
                Model.mongo_encode_obj(self)
                )
        else:
            collection.insert_one(Model.mongo_encode_obj(self))

    @classmethod
    def save_one(cls, obj):
        """."""
        mongoClient = MongoClient()
        db = mongoClient['rest_testing']
        collection = db[cls.__name__]
        collection.insert_one(Model.mongo_encode_obj(cls, obj))

    @classmethod
    def find(cls):
        """."""
        mongoClient = MongoClient()
        db = mongoClient['rest_testing']
        collection = db[cls.__name__]
        result = []
        for document in collection.find():
            result.append(Model.mongo_decode_obj(document, cls))
        return result

    def delete(self):
        """."""
        mongoClient = MongoClient()
        db = mongoClient['rest_testing']
        collection = db[type(self).__name__]
        if (
                hasattr(self, "_id") and
                collection.find({"_id": self._id}).count() > 0
                ):
            collection.delete_one({"_id": self._id})
        else:
            raise EntityDoesntExistException()

    @classmethod
    def delete_one(cls, obj):
        """."""
        mongoClient = MongoClient()
        db = mongoClient['rest_testing']
        collection = db[type(obj).__name__]
        if (
                hasattr(obj, "_id") and
                collection.find({"_id": obj._id}).count() > 0
                ):
            collection.delete_one({"_id": obj._id})
        else:
            raise EntityDoesntExistException()

    @classmethod
    def mongo_encode_obj(cls, obj):
        """."""
        encoded = {'_type': type(obj).__name__}
        for attr in vars(obj):
            encoded[attr] = obj.__getattribute__(attr)
        return encoded

    @classmethod
    def mongo_decode_obj(cls, doc, obj_type):
        """."""
        assert doc["_type"] == obj_type.__name__
        obj = obj_type()
        for attr in doc:
            obj.__setattr__(attr, doc[attr])
        return obj

    def json(self):
        """returns the class as a json"""
        return json.dumps(self.__dict__)


#
# Module Testing
#
if (__name__ == "__main__"):
    class TestModel(Model):
        """."""

        def __init__(self):
            """."""
            self.nombre = "Juan"
            self.apellido = "Perez"

    import os
    dirname, _ = os.path.split(os.path.abspath(__file__))
    print("running from", dirname)
    test = TestModel()
    test.save()
    tests = test.find()
    for test in tests:
        print(test.nombre, test.apellido)
    for key in vars(test):
        print(key, ": ", test.__getattribute__(key))
    test.delete()
