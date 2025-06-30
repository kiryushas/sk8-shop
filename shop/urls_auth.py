from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='product_list'), name='logout'),
    path('register/', views.register, name='register'),

    # Подключаем стандартные пути Django для аутентификации
    path('accounts/', include('django.contrib.auth.urls')),
]
