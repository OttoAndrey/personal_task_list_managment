from django.contrib import admin
from django.urls import path, include

from apps.router import router
from users.views import CustomAuthToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/login/', CustomAuthToken.as_view(), name='api-login'),
]
