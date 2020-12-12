from rest_framework.viewsets import ModelViewSet

from main.permissions.todo import IsOwnerPermission
from to_do.models import Todo
from to_do.serializers import TodoSerializer


class TodoViewSet(ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [IsOwnerPermission, ]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)
