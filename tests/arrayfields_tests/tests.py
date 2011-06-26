#coding=utf-8
from django.core import serializers
from django.db import DatabaseError
from django.test import TestCase
from .models import *

class SimpleTest(TestCase):
    def setUp(self):
        pass

    def test_text(self):
        item = Item.objects.create(text=['a', 'b'])
        self.assertEqual(
            item.pk,
            Item.objects.extra(where=['text[1]=%s'], params=['a']).get().pk,
        )

    def test_integer(self):
        item = Item.objects.create(integer=[[1,2], [1,2]])
        self.assertEqual(1, item.integer[1][0])

    def test_character_max_length(self):
        with self.assertRaisesRegexp(DatabaseError, 'value too long for type character varying'):
            item = Item.objects.create(char=['opq'])

    def test_serialization(self):
        item = Item.objects.create(text=[['abc'],['xyz']])
        s = serializers.serialize('json', list(Item.objects.all()))
        item.delete()
        s = s.replace('abc', 'def')
        for obj in serializers.deserialize('json', s):
            obj.save()
        self.assertEqual(Item.objects.get().text, [['def'],['xyz']])

