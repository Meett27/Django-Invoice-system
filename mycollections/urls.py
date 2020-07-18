from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

app_name = 'mycollections'

urlpatterns = [
	path('',login_required(views.HomepageView.as_view(),login_url='/'), name='homepage'),
	path('collection/<int:pk>/', login_required(views.CollectionDetailView.as_view(),login_url='/'), name='collection_detail'),
    path('collection/create/', login_required(views.CollectionCreate.as_view(),login_url='/'), name='collection_create'),
    path('collection/update/<int:pk>/', login_required(views.CollectionUpdate.as_view(),login_url='/'), name='collection_update'),
    path('collection/delete/<int:pk>/', login_required(views.CollectionDelete.as_view(),login_url='/'), name='collection_delete'),
    path('collection/upload/',login_required(views.UploadBookView.as_view(),login_url='/'),name='list'),
    path('upload/',login_required(views.upload,login_url='/'),name='upload'),
    path('collection/manager',login_required(views.CollectionListView.as_view(),login_url='/'),name='managerview')
	]
