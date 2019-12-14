from rest_framework.serializers import ModelSerializer
from webapp.models import Foto, Comments
from rest_framework import serializers



class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'text', 'fotocomment', 'author', 'created_at']


class FotoSerializer(serializers.ModelSerializer):
    comment_foto = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Foto
        fields = ('id', 'foto', 'subscribe', 'created_at',
                  'rating', 'user', 'comment_foto')