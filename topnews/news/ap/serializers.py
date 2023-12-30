from rest_framework.serializers import ModelSerializer
from news.models import Room

class RoomSerializers(ModelSerializer):
    class Meta:
        model = Room
        fields = ['id','host','topic','name']