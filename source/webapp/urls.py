from django.urls import path
from .views import IndexView, FotoView, FotoCreateView, FotoUpdateView, FotoDeleteView, login_view, logout_view

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('foto/<int:pk>/', FotoView.as_view(), name='foto_detail'),
    path('create/', FotoCreateView.as_view(), name='foto_create'),
    path('foto/<int:pk>/update/', FotoUpdateView.as_view(), name='foto_update'),
    path('foto/<int:pk>/delete/', FotoDeleteView.as_view(), name='foto_delete'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]