from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from news.models import Room
from rest_framework.views import APIView
from .serializers import RoomSerializers


@api_view(['GET'])
def getRoutes(request):
    route={
        'GET /ap'
        'GET /ap/rooms', 
        'GET /ap/rooms/:id'    
    } 
    return Response(route)

class roomlist(APIView):
    def get(self,request):
        rooms=Room.objects.all()
        serializer = RoomSerializers(rooms, many =True)
        return Response(serializer.data)
    # def get(self,requst,pk):
    #     rooms=get_object_or_404(Room,id=pk)
    #     serializer = RoomSerializers(rooms, many =False)
    #     return Response(serializer.data)
    def post(self,request):
        serializer=RoomSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.validated_data)
        return Response('ok')

# @api_view(['GET','POST'])
# def getRooms(request):
    # if request.method =='GET':  
    #     rooms=Room.objects.all()
    #     serializer = RoomSerializers(rooms, many =True)
    #     return Response(serializer.data)
    # elif request.method=='POST':
    #     serializer=RoomSerializers(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     print(serializer.validated_data)
    #     return Response('ok')
# @api_view(['GET'])
# def getRoom(request, pk):
#     rooms=get_object_or_404(Room,id=pk)
#     serializer = RoomSerializers(rooms, many =False)
#     return Response(serializer.data)
    
        
    