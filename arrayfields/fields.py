import json
from abc import abstractproperty
from django.db import models
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _


class ArrayFieldBase(models.Field):
    base_db_type = abstractproperty()

    def db_type(self, connection):
        return '%s[]' % self.base_db_type

    def get_prep_value(self, value):
        if value == '':
            value = '{}'
        return value

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return json.dumps(value)

    def to_python(self, value):
        if isinstance(value, basestring):
            value = json.loads(value)
        return value

    def south_field_triple(self):
        from south.modelsinspector import introspector
        name = '%s.%s' % (self.__class__.__module__ , self.__class__.__name__)
        args, kwargs = introspector(self)
        return name, args, kwargs


class CharArrayField(ArrayFieldBase):
    """
    A character varying array field for PostgreSQL
    """
    description = _('Character array')
    base_db_type = 'character varying'


class TextArrayField(ArrayFieldBase):
    """
    A text array field for PostgreSQL
    """
    description = _('Text array')
    base_db_type = 'text'


class IntegerArrayField(ArrayFieldBase):
    """
    An integer array field for PostgreSQL
    """
    description = _('Integer array')
    base_db_type = 'integer'

