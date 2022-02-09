from rest_framework import serializers

class CreateTableSerializer(serializers.Serializer):
    name = serializers.CharField(required = True)
    age = serializers.IntegerField(required = True)