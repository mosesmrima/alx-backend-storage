#!/usr/bin/env python3
"""python func that lists all documents in a collection"""
import pymongo


def list_all(mongo_collection):
    """
    list all docs in a collection
    """
    if not mongo_collection:
         return []
    return list(mongo_collection.find())