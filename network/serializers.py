from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .models import Message


class MessageSerializer(serializers.Serializer):
    fromWhom = serializers.CharField(max_length=50)
    toWhom = serializers.CharField(max_length=50)
    content = serializers.CharField(max_length=255)
    time_create = serializers.DateTimeField()
    time_update = serializers.DateTimeField()
    is_published = serializers.BooleanField(default=True)
    cat_id = serializers.IntegerField

    def create(self, validated_data):
        return Message.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.fromWhom = validated_data.get("fromWhom", instance.fromWhom)
        instance.toWhom = validated_data.get("toWhom", instance.toWhom)
        instance.content = validated_data.get("content", instance.content)
        instance.time_update = validated_data.get("time_update", instance.time_update)
        instance.is_published = validated_data.get("is_published", instance.is_published)
        instance.cat_id = validated_data.get("cat_id", instance.cat_id)
        instance.save()
        return instance


