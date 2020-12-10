from rest_framework.serializers import ModelSerializer

from to_do.models import Todo


class TodoSerializer(ModelSerializer):
    class Meta:
        model = Todo
        fields = ['title', 'text', 'completion_date', 'complete', 'user', ]
        extra_kwargs = {'user': {'read_only': True}, }

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
