from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, get_object_or_404
from .models import RewardsAppUsers, RewardsAppAndroidapp, RewardsAppUsertask
from .serializers import UserSerializer, AndroidAppSerializer, UserTaskSerializer
from django.contrib.auth import authenticate, login
from rest_framework import status
from django.utils.timezone import now
import json
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.hashers import check_password
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from rest_framework.permissions import BasePermission
from .permissions import IsAdminUserRole
from rest_framework.pagination import PageNumberPagination

class UserPagination(PageNumberPagination):
    page_size = 10  


# class HomeView(APIView):
#     # Disable authentication for the GET method (login page)
#     authentication_classes = []
#     permission_classes = [AllowAny]  # Allow access to the login view without being authenticated

#     def get(self, request):
#         template = 'login.html'
#         # Render the login page without checking for accepted media types
#         return render(request, template)


# Assuming you are using a custom user model, otherwise use `User` directly
# User = get_user_model()

class UserLoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        template = 'login.html'
        
        if 'signup' in request.GET:
            template = 'signup.html'  # Check if the signup button was clicked
        
        return render(request, template)
        
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            # user = User.objects.get(email=email)
            user = RewardsAppUsers.objects.filter(email=email).first()
        except RewardsAppUsers.DoesNotExist:
            print("ERROR")
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        user_data = UserSerializer(user).data
        user_pass =user_data.get('password')

        if not user or password != user_pass:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate or retrieve token for the user
        token, created = Token.objects.get_or_create(user=user)

        # Prepare user data to return as JSON
        user_data = UserSerializer(user).data
        response_data = {
            "token": token.key,
            "user": user_data
        }
        
        # Return JSON data, not the HTML template
        return Response(response_data, status=status.HTTP_200_OK)
    

# class UserLoginView(APIView):
#     def get(self, request):
#         template = 'login.html'
#         if request.accepted_media_type == 'text/html':
#             return render(request, template)
        
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         user = authenticate(request, email=email, password=password)
#         print("user: ", user)

#         if user is not None:
#             login(request, user)  # Initiates a session for the logged-in user
#             return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
#         return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)




class UserSignupView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        # This will render the signup.html page
        return render(request, 'signup.html')

    def post(self, request):
        email = request.data.get('email')
        check_email = RewardsAppUsers.objects.filter(email=email, is_delete=False)

        if check_email:
            return Response({"error": "Email id already exist"}, status=400)
        
        password = make_password(request.data.get('password')) # Hash password
        request.data['password'] = password
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User Created Successfully"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserSignupView(APIView):
#     def get(self, request):
#         template = 'signup.html'
#         if request.accepted_media_type == 'text/html':
#             return render(request, template)
        
#     def post(self, request):
#         print(request.data)
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "User Created Successfully"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class DashboardView(APIView):
#     permission_classes = [IsAuthenticated, IsAdminUserRole] 

#     def get(self, request):
#         # Admin-only dashboard logic here
#         return Response({"message": "Admin Dashboard"})


class DashboardView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        role = request.query_params.get("role")
        user_id = request.query_params.get("id")

        role = 'admin'

        if role == 'admin':
            try:
                # Gather admin-specific data
                total_apps = RewardsAppAndroidapp.objects.filter(is_delete=False).count()
                total_users = RewardsAppUsers.objects.filter(role='user', is_delete=False).count()
                total_submissions = RewardsAppUsertask.objects.count()
                data = {
                    "total_apps": total_apps,
                    "total_users": total_users,
                    "total_submissions": total_submissions
                }
            except:
                data = {
                    "total_apps": 0,
                    "total_users": 0,
                    "total_submissions": 0
                }
        else:
            try:
                # Gather user-specific data
                completed_tasks = RewardsAppUsertask.objects.filter(user=user_id, is_completed=True).count()
                pending_tasks = RewardsAppUsertask.objects.filter(user=user_id, is_completed=False).count()
                points_earned = sum(task.points_earned for task in RewardsAppUsertask.objects.filter(user=user_id, is_delete=False))
                data = {
                    "completed_tasks": completed_tasks,
                    "pending_tasks": pending_tasks,
                    "points_earned": points_earned
                }
            except:
                data = {
                    "completed_tasks": 0,
                    "pending_tasks": 0,
                    "points_earned": 0
                }
            

        # Return JSON response with data
        # return Response(data, status=status.HTTP_200_OK)

        json_data = json.dumps(data)
        template = '1admin-dashboard.html'

        # return render(request, template, json.loads(json_data))
        return render(request, template, data)
    



class AddAppView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Ensure only admin users can access this view
        if request.user.role != 'admin':
            return Response({"error": "You do not have permission to view this page."},
                            status=status.HTTP_403_FORBIDDEN)
        
        if request.accepted_media_type == 'text/html':
            return render(request, '2admin-addapp.html')

    def post(self, request):
        # Ensure only admin users can add new apps
        if request.user.role != 'admin':
            return Response({"error": "You do not have permission to add apps."},
                            status=status.HTTP_403_FORBIDDEN)
        
        # Proceed with saving the app if the user is an admin
        serializer = AndroidAppSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        # Ensure only admin users can update apps
        if request.user.role != 'admin':
            return Response({"error": "You do not have permission to update apps."},
                            status=status.HTTP_403_FORBIDDEN)
        
        # Fetch the app and update it if it exists and is not marked as deleted
        app = get_object_or_404(RewardsAppAndroidapp, pk=pk, is_delete=False)
        serializer = AndroidAppSerializer(app, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        # Ensure only admin users can delete apps
        if request.user.role != 'admin':
            return Response({"error": "You do not have permission to delete apps."},
                            status=status.HTTP_403_FORBIDDEN)
        
        # Soft delete the app by setting is_delete to True
        app = get_object_or_404(RewardsAppAndroidapp, pk=pk, is_delete=False)
        app.is_delete = True
        app.deleted_on = now()
        app.save()
        return Response({"message": "App marked as deleted"}, status=status.HTTP_200_OK)

# class AddAppView(APIView):
#     def get(self, request):
#         if request.accepted_media_type == 'text/html':
#             return render(request, '2admin-addapp.html')

#     def post(self, request):
#         serializer = AndroidAppSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UpdateAppView(APIView):
#     def patch(self, request, pk):
#         app = RewardsAppAndroidapp.objects.get(pk=pk, is_delete=False)
#         serializer = AndroidAppSerializer(app, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class DeleteAppView(APIView):
#     def delete(self, request, pk):
#         app = RewardsAppAndroidapp.objects.get(pk=pk)
#         app.is_delete = True
#         app.deleted_on = now()
#         app.save()
#         return Response({"message": "App marked as deleted"}, status=status.HTTP_200_OK)



class AssignedTasksView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserRole]
    pagination_class = UserPagination

    def get(self, request):
        # if request.user.role != 'admin':
        #     return Response({"error": "Permission denied. Admin access only."}, status=status.HTTP_403_FORBIDDEN)
        try:
            apps = RewardsAppAndroidapp.objects.filter(is_delete=False)
            
            # Use the pagination class to paginate the queryset
            paginator = self.pagination_class()
            paginated_apps = paginator.paginate_queryset(apps, request)
            serializer = AndroidAppSerializer(paginated_apps, many=True)
            
            # HTML response rendering
            if request.accepted_media_type == 'text/html':
                return render(request, 'apps_tasks.html', {'apps': serializer.data})

            # Paginated JSON response with pagination details
            return paginator.get_paginated_response(serializer.data)
            
        except Exception as e:
            # Handle errors gracefully
            if request.accepted_media_type == 'text/html':
                return render(request, '3admin-tasks.html')
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class AssignedTasksView(APIView):
#     def get(self, request):
#         try:
#             apps = RewardsAppAndroidapp.objects.filter(is_delete=False)
#             serializer = AndroidAppSerializer(apps, many=True)
#             if request.accepted_media_type == 'text/html':
#                 return render(request, 'apps_tasks.html', {'apps': serializer.data})
#             return Response(serializer.data)
#         except:
#             if request.accepted_media_type == 'text/html':
#                 return render(request, '3admin-tasks.html')


class UserListView(ListAPIView):
    queryset = RewardsAppUsers.objects.filter(role='user', is_delete=False)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]  # Only admins can access
    pagination_class = UserPagination  # Enable pagination

    def get_queryset(self):
        # Return only non-deleted users
        return RewardsAppUsers.objects.filter(is_delete=False)

# class UserListView(APIView):
#     def get(self, request):
#         try:
#             users = RewardsAppUsers.objects.filter(role='user', is_delete=False)
#             serializer = UserSerializer(users, many=True)

#             data = {'users': serializer.data}
#             json_data = json.dumps(data)

#             if request.accepted_media_type == 'text/html':
#                 return render(request, 'users_view.html', json.loads(json_data))
#             return Response(data)
#         except:
#             if request.accepted_media_type == 'text/html':
#                 return render(request, '4admin-usersview.html')



class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Ensuring that only authenticated users can access this view

    def get(self, request):
        user_id = request.query_params.get("id") or request.user.id  # Default to logged-in user if no 'id' is provided
        template = '5user-profile.html'
        
        try:
            user = RewardsAppUsers.objects.get(id=user_id)
            serializer = UserSerializer(user)
            if request.accepted_media_type == 'text/html':
                return render(request, template, {'user': serializer.data})
            return Response(serializer.data)
        except RewardsAppUsers.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Log unexpected errors
            print(f"Error occurred while fetching user: {e}")
            return Response({"error": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        user_id = request.query_params.get("id") or request.user.id  # Default to logged-in user if no 'id' is provided
        
        try:
            user = RewardsAppUsers.objects.get(id=user_id)
        except RewardsAppUsers.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the request contains a file (profile picture)
        if 'profilepic' in request.FILES:
            profilepic = request.FILES['profilepic']
            # Save the uploaded file to the 'media/profile_pics/' directory
            fs = FileSystemStorage(location='media/profile_pics/')
            filename = fs.save(profilepic.name, profilepic)  # Save the file
            request.data['profilepic'] = f'profile_pics/{filename}'  # Set the file path in the data

        # Update the user profile with the new data (partial update allowed)
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()  # Save the updated user data
            return Response(serializer.data)
        else:
            # Return validation errors if any
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserProfileView(APIView):
#     def get(self, request):
#         user_id = request.query_params.get("id")
#         template = '5user-profile.html'
#         try:
#             user = RewardsAppUsers.objects.get(id=user_id)
#             print(user)
#             serializer = UserSerializer(user)
#             if request.accepted_media_type == 'text/html':
#                 return render(request, template, {'user': serializer.data})
#             return Response(serializer.data)
#         except:
#             if request.accepted_media_type == 'text/html':
#                 return render(request, '5user-profile.html')

#     def patch(self, request):
#         user_id = request.query_params.get("id")
#         try:
#             user = RewardsAppUsers.objects.get(id=user_id)
#         except RewardsAppUsers.DoesNotExist:
#             return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

#         # Check if the request data contains a file
#         if 'profilepic' in request.FILES:
#             profilepic = request.FILES['profilepic']
#             # Save the uploaded file to the desired path
#             fs = FileSystemStorage(location='media/profile_pics/')
#             filename = fs.save(profilepic.name, profilepic)  # Save the file
#             request.data['profilepic'] = f'profile_pics/{filename}'  # Update the user object with the path

#         serializer = UserSerializer(user, data=request.data, partial=True)
#         print("here-----A------>")
#         print(request.data)
#         try:
#             if serializer.is_valid():
#                 print("here----B------->")
#                 serializer.save()
#                 return Response(serializer.data)
#         except Exception as e:
#             print("The error is: ",e)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ======================Just for testing==========================
class UserDataView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        # try:
        users = RewardsAppUsers.objects.filter().all()
        serializer = UserSerializer(users, many=True)

        data = {'users': serializer.data}

        # for usr in serializer.data:
        #     print("Email: ", usr['email'], "  Pass: ", usr['password'])
        
        json_data = json.dumps(data)

        # if request.accepted_media_type == 'text/html':
        #     return render(request, 'users_view.html', json.loads(json_data))
        return Response(data)
        # except:
        #     if request.accepted_media_type == 'text/html':
        #         return render(request, '4admin-usersview.html')