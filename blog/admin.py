from django.contrib import admin
from .models import Blog_db, Author, Tag, Comment
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("author", "blog_tags", 'date',)
    list_display = ("title", "date", "author",)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name", "post")
# class AuthorAdmin(admin.ModelAdmin):
#     list_filter = ("first_name",)
#     list_display = ("first_name", "last_name",)

# class TagAdmin(admin.ModelAdmin):
   
#     list_display = ("caption",)

admin.site.register(Blog_db, BlogAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
