from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count

from .models import Subscription, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'get_subscribers',
        'get_recipes'
    )
    list_filter = ('username', 'email')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            subscribers_amount=Count('following'),
            recipes_amount=Count('recipes')
        )
        return queryset

    @admin.display(description='Кол-во подписчиков')
    def get_subscribers(self, obj):
        return obj.subscribers_amount

    @admin.display(description='Кол-во рецептов')
    def get_recipes(self, obj):
        return obj.recipes_amount


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author'
    )
