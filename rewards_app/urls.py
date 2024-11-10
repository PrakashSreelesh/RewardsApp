from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # JWT token endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    #Landing Login page
    # path('', views.UserLoginView.as_view(), name='login'),

    # User authentication and signup
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('signup/', views.UserSignupView.as_view(), name='signup'),
    
    # Dashboard and app management
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('add-app/', views.AddAppView.as_view(), name='add_app'),
    path('update-app/<int:pk>/', views.AddAppView.as_view(), name='update_app'),
    path('delete-app/<int:pk>/', views.AddAppView.as_view(), name='delete_app'),
    
    # Assigned tasks
    path('assigned-tasks/', views.AssignedTasksView.as_view(), name='assigned_tasks'),
    
    # User-related views
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('userauth/', views.UserDataView.as_view(), name='user_data'),  # Just for testing, can be removed later
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files during development
