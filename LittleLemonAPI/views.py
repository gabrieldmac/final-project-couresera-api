from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

from django.contrib.auth.models import User, Group

# Create your views here.
@api_view()
def test(request):
    return Response('This is a test', status.HTTP_200_OK)

@api_view(['POST', 'DELETE', 'GET'])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name='Manager')
        if request.method == 'POST':
            managers.user_set.add(user)
            return Response({'message:':'User set to manager group'}, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            managers.user_set.remove(user)
            return Response({'message:':'User deleted from manager group'}, status=status.HTTP_200_OK)
    return Response({'message:':'There was a problem in this endpoint'}, status=status.HTTP_400_BAD_REQUEST)