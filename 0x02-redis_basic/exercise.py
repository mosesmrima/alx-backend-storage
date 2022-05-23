#!/usr/bin/env python3
"""
Define a class Cache that deals with redis database operations
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function
    """
    name = method.__qualname__
    r = method.__self__._redis
    count = r.get(name).decode('utf-8')
    print("{} was called {} times:".format(name, count))
    inputs = r.lrange("{}:inputs".format(name), 0, -1)
    outputs = r.lrange("{}:outputs".format(name), 0, -1)
    res = zip(inputs, outputs)
    for i, o in res:
        i = i.decode('utf-8')
        o = o.decode('utf-8')
        print("{}(*{}) -> {}".format(name, i, o))


def call_history(method: Callable) -> Callable:
    """
    Takes a callable argument and returns a callable
    """
    @wraps(method)
    def history(self, *args, **kwargs):
        """
        Store history of inputs and outputs for a function
        """
        name = method.__qualname__
        self._redis.rpush("{}:inputs".format(name), str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush("{}:outputs".format(name), result)
        return result
    return history


def count_calls(method: Callable) -> Callable:
    """
    Takes a callable argument and returns a callable
    """
    @wraps(method)
    def counter(self, *args, **kwargs):
        """
        Count howm many times a method is called
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return counter


class Cache:
    """
    Create an instance of a Redis client and flush it using flushdb
    """
    def __init__(self):
        """
        Create an instance of a Redis client and flush it using flushdb
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in Redis with a randomly-generated key and returns the key
        Args:
            data (str, bytes, int, float): data to be stored
        """
        key: uuid.UUID = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self: redis.Redis, key: str, fn: Optional[Callable]
            = None) -> Union[str, bytes, int, float]:
        """
        Makes a get request to Redis using the provided key and converts the
        result to the desired format using the function passed
        Args:
            key (str): key whose value is to be retrieved
            fn (callable): function to convert returned value to desired format
        """
        val = self._redis.get(key)
        if fn is not None:
            val_conv = fn(val)
            return val_conv
        return val

    def get_str(self, key: str) -> str:
        """
        Get data from Redis and return in str format
        Args:
            key (str): key to retrieve data for
        Returns:
            str: data
        """
        data = self.get(key, lambda x: x.decode('utf-8'))
        return data

    def get_int(self, key: str) -> int:
        """
        Get data from Redis and return in int format
        Args:
            key (str): key to retrieve data for
        Returns:
            int: data
        """
        data = self.get(key, lambda x: int(x))
        return data
