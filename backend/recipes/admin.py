from django.contrib import admin
from django.utils.safestring import mark_safe

from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    fields = ('ingredient', 'amount')
    min = 1
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('measurement_unit',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_ingredients', 'get_image', 'author')
    list_filter = ('author', 'name', 'tags')
    inlines = (IngredientRecipeInline,)

    @admin.display(description='Ингредиенты')
    def get_ingredients(self, obj):
        return ', '.join(
            (ingredient.name for ingredient in obj.ingredients.all())
        )

    @admin.display(description='Изображение')
    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width=75>')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_colored_tag', 'slug')
    search_fields = ('name',)

    @admin.display(description='Цвет в HEX')
    def get_colored_tag(self, obj):
        return mark_safe(f'<span style="color:{obj.color}">{obj.color}</span>')


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
    list_editable = ('amount',)
    search_fields = ('ingredient',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    list_editable = ('user', 'recipe')
    list_filter = ('user',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    list_editable = ('user', 'recipe')
    list_filter = ('user',)
