from rest_framework.pagination import PageNumberPagination

from .constants import ITEMS_PER_PAGE


class CustomPagination(PageNumberPagination):
    page_size = ITEMS_PER_PAGE
    page_size_query_param = 'limit'
