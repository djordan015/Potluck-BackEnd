from django.apps import AppConfig


class MongoConfig(AppConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'
    name = 'mongo'
