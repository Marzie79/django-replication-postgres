import random

from django.db import connections
from django.db.utils import OperationalError


class MainRouter:
    """A router to control read and write database operations on models."""

    @staticmethod
    def connection_status(database='default'):
        """Try to find a database that is available."""
        status = True
        db_connection = connections[database]
        try:
            db_connection.cursor()
        except OperationalError:
            status = False
        finally:
            return status

    def db_for_read(self, model, **hints):
        """Point all operations randomly on all models to replica1 or replica2."""
        database = random.choice(['replica1', 'replica2'])

        if self.connection_status(database=database):
            return database
        else:
            self.db_for_read(self)

    def db_for_write(self, model, **hints):
        """Point all operations on all models to default."""
        return "default"
