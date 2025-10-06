from django.db import models
from django.conf import settings
from django_mongodb_backend.fields import EmbeddedModelField, ArrayField
from django_mongodb_backend.models import EmbeddedModel


class Sample(models.Model):
    name = models.CharField(max_length=200)
    
    class Meta:
        db_table = "sample"
        managed = False
        
    def __str__(self):
        return self.name
    

    