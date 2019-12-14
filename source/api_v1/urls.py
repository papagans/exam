from django.urls import include, path
from rest_framework import routers
from api_v1 import views
from rest_framework.authtoken.views import obtain_auth_token

from api_v1.views import LogoutView

router = routers.DefaultRouter()
router.register(r'foto', views.FotoViewSet)
router.register(r'comments', views.CommentViewSet)
app_name = 'api_v1'

urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('logout/', LogoutView.as_view(), name='api_token_delete')
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]