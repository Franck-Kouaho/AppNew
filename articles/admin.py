from django.contrib import admin
from django.http import HttpRequest

from articles.models import Category, SubCategory, Article, Like, Notifications, Respons

# Register your models here.
admin.site.register(Notifications)
admin.site.register(Like)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display= ("__str__", "get_subcategorie_number", "get_article_number")
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by()

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display= ("__str__", 'category' ,"get_article_number")
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by()

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display= ("__str__", "get_like_number", "get_dislike_number", "get_respons_number", "get_followers_numbers")
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(articleParent=None)

@admin.register(Respons)
class ArticleResponsAdmin(admin.ModelAdmin):
    list_display= ("__str__", "get_like_number", "get_dislike_number", "get_respons_number", "get_followers_numbers")
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(articleParent=None)