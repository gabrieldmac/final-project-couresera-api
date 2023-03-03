from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import MenuItem

from django.contrib.auth.models import User, Group


# User section
@api_view(['POST', 'DELETE', 'GET'])
@permission_classes([IsAuthenticated])
def managers(request):
    try:
        username = request.data['username']
    except:
        return Response({'message:':'please send the username parameter'}, status=status.HTTP_400_BAD_REQUEST)
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name='Manager')
        if not validate_role('Manager', managers, username):
            return Response({'message:':'You do not have access to this endpoint'}, status=status.HTTP_403_FORBIDDEN)
        if request.method == 'POST':
            managers.user_set.add(user)
            return Response({'message:':'User set to manager group'}, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            managers.user_set.remove(user)
            return Response({'message:':'User deleted from manager group'}, status=status.HTTP_200_OK)
        elif request.method == 'GET':
            all_managers = managers.user_set.all().values()
            if all_managers:
                return Response({'data:':list(all_managers)}, status=status.HTTP_200_OK)
    return Response({'message:':'We could not find that user'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', 'DELETE', 'GET'])
@permission_classes([IsAuthenticated])
def delivery_crew(request):
    try:
        username = request.data['username']
    except:
        return Response({'message:':'please send the username parameter'}, status=status.HTTP_400_BAD_REQUEST)
    
    if username:
        user = get_object_or_404(User, username=username)
        delivery_crew = Group.objects.get(name='Delivery Crew')
        if not validate_role('Delivery Crew', delivery_crew, username):
            return Response({'message:':'You do not have access to this endpoint'}, status=status.HTTP_403_FORBIDDEN)
        if request.method == 'POST':
            delivery_crew.user_set.add(user)
            return Response({'message:':'User set to Delivery Crew Group'}, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            delivery_crew.user_set.remove(user)
            return Response({'message:':'User deleted from Delivery Crew group'}, status=status.HTTP_200_OK)
        elif request.method == 'GET':
            all_delivery_crew = delivery_crew.user_set.all().values()
            if all_delivery_crew:
                return Response({'data:':list(all_delivery_crew)}, status=status.HTTP_200_OK)
    return Response({'message:':'We could not find that user'}, status=status.HTTP_404_NOT_FOUND)





# menu items section
@api_view(['POST', 'DELETE', 'GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def menu_items(request):
    try:
        username = request.data['username']
    except:
        return Response({'message:':'please send the username parameter'}, status=status.HTTP_400_BAD_REQUEST)
    
    managers = Group.objects.get(name='Manager')
    
    if username: 
        if validate_role('Manager', managers, username):
            
            menu = MenuItem.objects.all().values()
            return Response({'message:':'it is a manager', 'data' : menu}, status=status.HTTP_200_OK)
        else:
            pass

    return Response({'message:':'We could not find that user'}, status=status.HTTP_404_NOT_FOUND)





def validate_role(role, user_list,user_name):
    if role == 'Manager':
        filtered_users = user_list.user_set.filter(username=user_name)
        if filtered_users:
            return True
        return False
    if role == 'Delivery Crew':
        filtered_users = user_list.user_set.filter(username=user_name)
        if filtered_users:
            return True
        return False