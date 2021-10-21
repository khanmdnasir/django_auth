from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include
from users import views
from users.forms import AuthenticationForm,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView,PasswordChangeDoneView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('',views.home,name="home"),
    path('accounts/password_change',PasswordChangeView.as_view(template_name='users/changepassword.html',form_class=MyPasswordChangeForm),name="changepassword"),
    path('accounts/password_change/done',PasswordChangeDoneView.as_view(template_name='users/passChangeDone.html'),name="password_change_done"),
    path('accounts/password_reset/',PasswordResetView.as_view(template_name="users/password_reset.html",form_class=MyPasswordResetForm),name="password_reset"),
    path('accounts/password_reset/done/',PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),name="password_reset_done"),
    path('accounts/reset/done/',PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),name="password_reset_complete"),
    path('accounts/reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html",form_class=MySetPasswordForm),name="password_reset_confirm"),
    
    path('login/',views.login_view,name='login'),
    # path('accounts/login/', LoginView.as_view(template_name='app/login.html',authentication_form=AuthenticationForm), name='login'),
    path('accounts/logout/',LogoutView.as_view(),name='logout'),
    # path('registration/', views.customerregistration, name='customerregistration'),
    path('registration/', views.registration_view, name='registration'),
    path('activate-user/<uidb64>/<token>',
         views.activate_user, name='activate'),
    path('activate/<uid>/<token>',
         views.activate_email, name='activate_email'),
    
    path('verify/',views.verify_view,name='verify')
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
