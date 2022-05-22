#!/usr/bin/env python3
"""return the list of school having a specific topic"""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    return a list
    """
    return mongo_collection.find({"topics": topic})