from django.core.validators import MinValueValidator
from django.db import models

from users.models import User
from .validators import validate_color
from foodgram.constants import (MAX_INGREDIENT_MEASUREMENT_UNIT_LENGTH,
                                MAX_INGREDIENT_NAME_LENGTH,
                                MAX_RECIPE_NAME_LENGTH, MAX_TAG_COLOR_LENGTH,
                                MAX_TAG_NAME_LENGTH, MAX_TAG_SLUG_LENGTH,
                                MIN_COOKING_TIME_IN_MINUTES,
                                MIN_INGREDIENTS_AMOUNT)


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        max_length=MAX_INGREDIENT_NAME_LENGTH,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=MAX_INGREDIENT_MEASUREMENT_UNIT_LENGTH,
        verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient_measurement_unit'
            )
        ]

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(
        max_length=MAX_TAG_NAME_LENGTH,
        verbose_name='Название',
        unique=True
    )
    color = models.CharField(
        max_length=MAX_TAG_COLOR_LENGTH,
        null=True,
        verbose_name='Цвет в HEX',
        help_text='Укажите цветовой код в HEX (например, #E26C2D)',
        validators=[validate_color],
    )
    slug = models.SlugField(
        max_length=MAX_TAG_SLUG_LENGTH,
        null=True,
        verbose_name='Слаг',
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=MAX_RECIPE_NAME_LENGTH,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Изображение',
        null=False,
        blank=False
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты',
        related_name='recipes',
        blank=False
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(
            MIN_COOKING_TIME_IN_MINUTES,
            'Время приготовления не может быть меньше 1 минуты.'
        )],
        verbose_name='Время приготовления в минутах'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    """Связующая модель ингредиентов в рецепте."""

    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(
            MIN_INGREDIENTS_AMOUNT, 'Количество не может быть менее 1.'
        )],
        verbose_name='Количество'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredients_in_recipe'
            )
        ]

    def __str__(self):
        return f'{self.recipe.name}: {self.ingredient.name}'


class FavoriteShoppingCartBaseModel(models.Model):
    """
    Базовый класс для добавления рецептов в избранное
    и списка покупок.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        abstract = True


class Favorite(FavoriteShoppingCartBaseModel):
    """Модель добавления рецептов в избранное."""

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        default_related_name = 'favorites'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_favorite_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'


class ShoppingCart(FavoriteShoppingCartBaseModel):
    """Модель списка покупок."""

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        default_related_name = 'cart'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_cart'
            )
        ]

    def __str__(self):
        return f'{self.recipe.name} в списке у {self.user.username}'
