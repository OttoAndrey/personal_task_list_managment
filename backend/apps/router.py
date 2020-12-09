from rest_framework import routers

from users.views import UsersViewSet

router = routers.DefaultRouter()
router.register('registration', UsersViewSet, basename='registration')
