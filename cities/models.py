from django.db import models
from django.db.models import Model, TextField, JSONField


class GameState(Model):
    name = TextField()
    state = JSONField()

# Create your models here.
