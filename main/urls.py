from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('',views.homepage, name='homepage'),
    # path("activate/<uidb64>/<token>/",views.activate, name='activate'),
    path('about/',views.about,name='about'),
    path('login/',views.login_request,name='login'),
    path('logout/',views.logout_request,name='logout'),
    path('register/',views.register,name='register'),
    path('user/',views.user_page,name="user_page"),
    path('delete_token/<int:pk>/', views.delete_token, name='delete_token'),
    # path("upload/<source>/",views.upload,name='upload'),
    path("upload/<str:folder>/",views.upload,name='upload'),

    path('folders/<slug:slug>/', views.folder_detail, name='folder_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)