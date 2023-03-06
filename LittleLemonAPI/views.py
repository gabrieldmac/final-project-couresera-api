from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import MenuItem, Category, Cart
from .serializers import MenuItemSerializer
from rest_framework.authtoken.models import Token



from django.contrib.auth.models import User, Group


# User section
@api_view(['POST', 'DELETE', 'GET'])
@permission_classes([IsAuthenticated])
def managers(request):
    try:
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)
        perm = user.groups.get()
        
    except:
        return Response({'message:':'We could not find that user'}, status=status.HTTP_404_NOT_FOUND)
    
    if user: 
        if perm.name != 'Manager':
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
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)
        perm = user.groups.get()
        
    except:
        return Response({'message:':'We could not find that user'}, status=status.HTTP_404_NOT_FOUND)
    
    if user: 
        delivery_crew = Group.objects.get(name='Delivery Crew')
        if not perm.name != 'Delivery Crew':
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
@api_view(['POST', 'GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def menu_items(request):

    try:
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)
    
    except Exception as e:
        return Response({'message:':'We could not find that user1'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        perm = user.groups.get()
    except:
        perm = None
    
    if user: 
        # Get has the same result for everyone
        if request.method == 'GET':
                menu = MenuItem.objects.all().values()
                return Response({'data' : menu}, status=status.HTTP_200_OK)
        
        # if it is a manager
        if perm is not None and perm.name == 'Manager':
            print('ROLE VALIDADO')
            if request.method == 'POST' :
                # creates a menu item
                try:
                    title = request.data['title']
                    price = request.data['price']
                    featured = request.data['featured']
                    categoryId = request.data['categoryId']
                    category = Category.objects.get(id = categoryId)
                    item = MenuItem(title = title, price = price, featured = featured, category = category)
                    item.save()
                    return Response(status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({'message:':'please make sure you are sending all paramenters', 'exception' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
                     
            elif request.method == 'PUT' or request.method == 'PATCH':
                 try:
                    item = MenuItem.objects.get(id = request.data['itemId'])
                    if item:
                        title = request.data['title']
                        price = request.data['price']
                        featured = request.data['featured']
                        categoryId = request.data['categoryId']
                        category = Category.objects.get(id = categoryId)
                        item = MenuItem(title = title, price = price, featured = featured, category = category)
                        item.save()
                        return Response(status=status.HTTP_201_CREATED)
                    else:
                        return Response({'message:':'could not find that item'}, status=status.HTTP_404_NOT_FOUND)
                 except KeyError as e:
                    return Response({'message:':'keyerror', 'exception' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
                 except Exception as e:
                    return Response({'message:':'please make sure you are sending at least one field', 'exception' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            if request.method == 'POST' or request.method == 'PUT' or request.method == 'PATCH':
                return Response({'message:':'You do not have access to this endpoint'}, status=status.HTTP_403_FORBIDDEN)
             
    return Response({'message:':'We could not find that user'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE', 'GET'])
@permission_classes([IsAuthenticated])
def single_menu_item(request, menu_item_id):
    try:
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)
        perm = user.groups.get()
        
    except:
        return Response({'message:':'We could not find that user'}, status=status.HTTP_404_NOT_FOUND)
    
    if user: 
        # Get has the same result for everyone
        if request.method == 'GET':
                item = get_object_or_404(MenuItem, pk=menu_item_id)
                serialized_item = MenuItemSerializer(item)
                return Response({'data':serialized_item.data}, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
                #if it is a manager:
                if perm.name == 'Manager':
                    item = get_object_or_404(MenuItem, pk=menu_item_id)
                    item.delete()
                    return Response({'message:':f'item with id {menu_item_id} deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({'message:':'You do not have access to this endpoint'}, status=status.HTTP_403_FORBIDDEN)

    return Response({ "error" : "error"}, status.HTTP_400_BAD_REQUEST )


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart_items(request):
    if request.method == 'GET':
        menu = Cart.objects.all().values()
        return Response({'data' : menu}, status=status.HTTP_200_OK)
    if request.method == 'POST':
        try:
            user = request.data['title']
            menuItem = request.data['price']
            quantity = request.data['featured']
            unit_price = request.data['categoryId']
            item = Cart(user = user, menuitem = menuItem, quantity = quantity, unit_price = unit_price)
            item.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message:':'please make sure you are sending all paramenters', 'exception' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
                     
