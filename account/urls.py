from django.urls import path
from account.views import (
    DashboardHome,
    logout_request,
    login_view,
    CreatePostView,
    CreateCategoryView,
    ProfileUpdate,
    UpdatePostView,
    DeletePostView,
    DeleteUserView,
    AllUserView,
    # users_edit
    EditUsersView,
    # password reset
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
    PasswordChangeView,
)

# change password 
from django.contrib.auth.views import PasswordChangeView

app_name = 'account'

urlpatterns = [
    path('account/dashboard/', DashboardHome.as_view(), name='home'),

    path('account/logout/', logout_request, name='logout'),
    
    path('account/login/', login_view, name='login'),
    
    path('account/create/', CreatePostView.as_view(), name='create'),
    
    path('account/create-category/', CreateCategoryView.as_view(), name='create-category'),

    path('account/update-post/<int:pk>/', UpdatePostView.as_view(), name='post-update'),

    path('account/update-profile/', ProfileUpdate.as_view(), name='profile-update'),

    path('account/change-password/', PasswordChangeView.as_view(), name='change-password'),

    path('account/delete-post/<int:pk>/', DeletePostView.as_view(), name='delete'),

    path('account/delete-user/<int:pk>/', DeleteUserView.as_view(), name='delete-user'),

    path('account/all-user/', AllUserView.as_view(), name='all-user'),
    
    path('account/edit/<int:pk>/', EditUsersView.as_view(), name='users-update'),

    # passwrod reset
    path('password-reset/', PasswordResetView.as_view(), name='pass-reset'),

    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),

    path('password-done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]



