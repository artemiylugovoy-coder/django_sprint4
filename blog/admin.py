# Register your models here.
from django.contrib import admin
from .models import Category, Post, Location, Profile
from django.contrib.auth.admin import UserAdmin


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'description',
                    'is_published',
                    'created_at'
                    )
    list_editable = ('description',
                     'is_published'
                     )


class PostAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'text',
                    'pub_date',
                    'author',
                    'location',
                    'category',
                    'is_published',
                    'created_at'
                    )
    list_editable = ('text',
                     'author',
                     'location',
                     'category',
                     'is_published',
                     )
    search_fields = ('title',)
    list_filter = ('category',)


class PostAdminInline(admin.TabularInline):
    model = PostAdmin
    extra = 0


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'is_published',
                    'created_at')
    list_editable = ('is_published',)


admin.site.empty_value_display = 'Не задано (◕‿◕)'
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Location, LocationAdmin)
