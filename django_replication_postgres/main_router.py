import random

from django.db import connections
from django.db.utils import OperationalError


class MainRouter:
    """A router to control read and write database operations on models."""

    def __init__(self) -> None:
        self.__databases = {'replica1', 'replica2'}
        self.__available_databases = {'replica1', 'replica2'}
        self.__default_database = "default"

    @staticmethod
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

    def _select_database(self) -> str:
        """Select a random database from available databases.

        Returns:
            The selected database.
        """
        if not self.__available_databases:
            return self.__default_database
        return random.choice(list(self.__available_databases))

    def _reset_availabe_databases(self):
        """Reset available database to its first condition."""
        self.__available_databases = self.__databases.copy()

    def db_for_read(self, model, **hints):
        """Point all operations on all models to an available database."""
        database = self._select_database()
        if self._connection_status(database=database):
            self._reset_availabe_databases()
            return database
        elif database != self.__default_database:
            self.__available_databases.remove(database)
            self.db_for_read(self)
        else:
            self._reset_availabe_databases()
            raise ConnectionError()

    def db_for_write(self, model, **hints):
        """Point all operations on all models to default."""
        return self.__available_databases
