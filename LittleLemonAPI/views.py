from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import MenuItem, Category, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, OrderSerializer
from rest_framework.authtoken.models import Token
from datetime import datetime
import random



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


@api_view(['DELETE', 'GET', 'POST', 'PATCH', 'PUT'])
@permission_classes([IsAuthenticated])
def single_menu_item(request, menu_item_id):
    # Double checking if user exists
    try:
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)
        
    except:
        return Response({'message:':'We could not find that user'}, status=status.HTTP_404_NOT_FOUND)
    
    # Checking if user has a group, if not it's a customer, so return None
    try:
        perm = user.groups.get()
    except:
        perm = None
    
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

# Cart Section
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart_items(request):
    if request.method == 'GET':
        
        user_id = Token.objects.get(key=request.auth.key).user_id
        cart = Cart.objects.filter(user_id = user_id).values()
        return Response({'data' : cart}, status=status.HTTP_200_OK)
    if request.method == 'POST':
        try:
            user = Token.objects.get(key=request.auth.key).user
            menu_item_id = request.data['menuItemId']
            menuItem = get_object_or_404(MenuItem, pk=menu_item_id)
            quantity = request.data['quantity']
            unit_price = menuItem.price
            price = int(quantity) * int(unit_price)
            item = Cart(user = user, menuitem = menuItem, quantity = quantity, unit_price = unit_price, price = price)
            item.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message:':'please make sure you are sending all paramenters', 'exception' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        try:
            user_id = Token.objects.get(key=request.auth.key).user_id
            cart = Cart.objects.filter(user_id = user_id)
            cart.delete()
            return Response({'message:':'Cart deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'message:':'please make sure you are sending all paramenters', 'exception' : str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Order Section

@api_view(['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def orders(request):
    # Double checking if user exists
    try:
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)

    except:
        return Response({'message:':'We could not find that user'}, status=status.HTTP_404_NOT_FOUND)
    
    # Checking if user has a group, if not it's a customer, so return None
    try:
        perm = user.groups.get()
    except:
        perm = None
    
    if request.method == 'GET':
        # For Customers
        if perm == None:
            user_id = Token.objects.get(key=request.auth.key).user_id
            orders = Order.objects.filter(user_id = user_id).values()
            return Response({'data' : orders}, status=status.HTTP_200_OK)
        # For Delivery Crew
        if perm.name == 'Delivery Crew':
            user_id = Token.objects.get(key=request.auth.key).user_id
            orders = Order.objects.filter(delivery_crew = user_id).values()
            return Response({'data' : orders}, status=status.HTTP_200_OK)

        # For Managers
        if perm.name == 'Manager':
            orders = Order.objects.all().values()
            return Response({'data' : orders}, status=status.HTTP_200_OK)
    if request.method == 'POST':
        if perm == None:
            # Return all cart items from the current user
            try:
                user_id = Token.objects.get(key=request.auth.key).user_id
                cart_object = Cart.objects.filter(user_id = user_id)
                cart = cart_object.values()
                total_cart_price = 0
                for item in cart:
                    total_cart_price = total_cart_price + item.get('price')
                order = Order(user = user, delivery_crew = None, status = 0, total = total_cart_price,  date = datetime.now())                
                order.save()

                for item in cart:
                    menuitem = MenuItem.objects.get(id=item.get('menuitem_id'))

                    order_item = OrderItem(order = order, menuitem = menuitem, quantity = item.get('quantity'), unit_price = item.get('unit_price'), price = item.get('price'))
                    order_item.save()

                print('BEFORE DELETE CART')
                cart_object.delete()

                return Response(status=status.HTTP_201_CREATED)


            except Exception as e:
                return Response({'message:':'generic error', 'exception' : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



            



        else:
            return Response({'message:':'You do not have access to this endpoint'}, status=status.HTTP_403_FORBIDDEN)

        
@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def single_order(request, order_id):
    # Double checking if user exists
    try:
        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)

    except:
        return Response({'message:':'We could not find that user'}, status=status.HTTP_404_NOT_FOUND)
    
    # Checking if user has a group, if not it's a customer, so return None
    try:
        perm = user.groups.get()
    except:
        perm = None
    
    # getting the order object
    order = get_object_or_404(Order, pk=order_id)
    
    if perm == None and request.method == 'GET':
        
        serialized_order = OrderSerializer(order)
        return Response({'data':serialized_order.data}, status=status.HTTP_200_OK)

    elif perm.name == 'Manager' and (request.method == 'PUT' or request.method == 'PATCH'):
        delivery_crew_users = list(User.objects.filter(groups__name__in=['Delivery Crew']))
        delivery_crew = random.sample(delivery_crew_users,1)[0]
        

        if order.delivery_crew == None:
            order.delivery_crew = delivery_crew
            order.status = True
            order.save()
            return Response({"message": f"Delivery crew assigned: {delivery_crew.username}"}, status=status.HTTP_202_ACCEPTED)
        elif order.status == True:
            return Response({'message': 'Order already delivered'}, status=status.HTTP_202_ACCEPTED)
        elif order.status == False:
            order.status = True
            order.save()
            return Response({'message': 'Order going to deliver'},status=status.HTTP_202_ACCEPTED)
        else: 
            return Response({'message:':'generic error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif perm.name == 'Delivery Crew' and request.method == 'PATCH':
        if order.status == False:
            order.status = True
            order.save()
            return Response({'message': 'Confirmed that order is delivered'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'message': 'Order was already delivered or does not exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    elif perm.name == 'Manager' and request.method == 'DELETE':
        try:
            order.delete()
        except Exception as e:
            return Response({'message:':'There was a problem deleting this order', 'exception' : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({'message:':'Cart deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
