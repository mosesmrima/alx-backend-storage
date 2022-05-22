#!/usr/bin/env python3
"""pyhton func that changes all topics of a school doc based on the name"""
import pymongo


def update_topics(mongo_collection, name, topics):
    """
    change all topics of a school doc
    """
    new_doc = mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
    return new_doc