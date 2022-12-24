import random

from django.db import connections
from django.db.utils import OperationalError


def _connection_status(database='default') -> bool:
    """Try to find a database that is available.

    Args:
        database: The database name that we want to test connection.

    Returns:
        The status of database connection.
    """
    try:
        connections[database].cursor()
        return True
    except OperationalError:
        return False


def _select_database(databases: list) -> str:
    """Select a random database from databases.

    Args:
        databases: The list of databases.

    Returns:
        The selected database.
    """
    return random.choice(databases)


def _pong(databases: list, default: str) -> str:
    """Select a random database from databases.

    Args:
        databases: The list of databases.
        default: The default database.

    Returns:
        The selected database.
    """
    if not databases:
        return default

    database = _select_database(databases)
    databases.remove(database)

    if _connection_status(database):
        return database

    return _pong(databases=databases, default=default)


def ping(fun):
    """Select a connectionable database."""
    def wrapper(*args, **kwargs):
        data = fun(*args, **kwargs)
        return _pong(databases=data['databases'], default=data["default"])
    return wrapper
