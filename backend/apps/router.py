from rest_framework import routers

from to_do.views import TodoViewSet
from users.views import UsersViewSet

router = routers.DefaultRouter()
router.register('registration', UsersViewSet, basename='registration')
router.register('todo', TodoViewSet, basename='todo')
