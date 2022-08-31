from django.contrib import admin
from .models import Author, Blog,Tag,Category,Review

# Register your models here.

admin.site.register(Author)
admin.site.register(Blog)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Review)