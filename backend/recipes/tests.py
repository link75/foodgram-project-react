from django.test import TestCase

from recipes.models import Ingredient


class IngredientModelTestCase(TestCase):

    def test_smoke(self):
        Ingredient.objects.create(name='salt', measurement_unit='gr')
