#!/usr/bin/env python3
"""python func that inserts a new doc"""

import pymongo


def insert_school(mongo_collection, **kwargs):
    """
    insert a new doc in a collection based on kwargs
    """
    new_doc = mongo_collection.insert_one(kwargs)
    return new_doc.inserted_id