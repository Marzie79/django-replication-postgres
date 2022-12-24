from django.conf import settings

from django_replication_postgres.connection import ping


class MainRouter:
    """A router to control read and write database operations on models."""

    @ping
    def db_for_read(self, model, **hints):
        """Point all operations on all models to an available database."""
        dbs_ = list(settings.DATABASES.keys())
        return {"default": dbs_.pop(0), "databases": dbs_}

    def db_for_write(self, model, **hints):
        """Point all operations on all models to default."""
        return list(settings.DATABASES.keys()).pop(0)
