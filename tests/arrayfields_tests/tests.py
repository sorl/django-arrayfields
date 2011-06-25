#coding=utf-8
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

    def test_serialization(self):
        item = Item.objects.create(char=['abc'])
        self.assertEqual(
            '["abc"]',
            item._meta.get_field('char').value_to_string(item)
            )

