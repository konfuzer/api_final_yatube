from django.contrib import admin

from .models import Comment, Follow, Group, Post


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    empty_value_display = '-пусто-'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('text', 'pub_date', 'author', 'group')
    search_fields = ('text', 'author__username', 'group__title')
    list_filter = ('pub_date', 'group')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'text', 'created')
    search_fields = ('text', 'author__username', 'post__text')
    list_filter = ('created',)
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')
    search_fields = ('user__username', 'following__username')
    empty_value_display = '-пусто-'
