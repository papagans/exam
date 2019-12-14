from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from webapp.models import Foto, Comments
from api_v1.serializers import FotoSerializer, CommentSerializer
from django.views.decorators.csrf import ensure_csrf_cookie

from django.utils.decorators import method_decorator


@method_decorator(ensure_csrf_cookie, name='dispatch')


class FotoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Foto.objects.all()
    serializer_class = FotoSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Foto.objects.all()
        return Foto.objects.all()

    def get_permissions(self):
        if self.action not in ['update', 'partial_update', 'destroy']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(methods=['post'], detail=True)
    def rate_up(self, request, pk=None):
        foto = self.get_object()
        foto.rating += 1
        foto.save()
        return Response({'id': foto.pk, 'rating': foto.rating})

    @action(methods=['post'], detail=True)
    def rate_down(self, request, pk=None):
        foto = self.get_object()
        foto.rating -= 1
        foto.save()
        return Response({'id': foto.pk, 'rating': foto.rating})


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer


class LogoutView(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user.auth_token.delete()
        return Response({'status': 'ok'})