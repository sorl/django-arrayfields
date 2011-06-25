from django.db import models
from arrayfields import TextArrayField, CharArrayField, IntegerArrayField


class Item(models.Model):
    text = TextArrayField()
    char = CharArrayField()
    integer = IntegerArrayField()

