from django.contrib import admin
from webapp.models import Foto, Comments


class FotoAdmin(admin.ModelAdmin):
    fields = ('foto', 'subscribe', 'rating', 'user')


class CommentsAdmin(admin.ModelAdmin):
    model = Comments
    fields = ('text', 'fotocomment', 'author')


admin.site.register(Foto, FotoAdmin)
admin.site.register(Comments, CommentsAdmin)