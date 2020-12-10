from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from main.permissions.todo import IsOwnerPermission
from to_do.models import Todo
from to_do.serializers import TodoSerializer


class TodoViewSet(ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = [IsOwnerPermission, ]

    def list(self, request, *args, **kwargs):
        queryset = Todo.objects.filter(user=request.user)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
