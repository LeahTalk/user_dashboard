from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^new$', views.new_user),
    url(r'^edit_user/(?P<user_id>\d+)/(?P<form_type>\w+)$', views.process_user_edits),
    url(r'^edit_password/(?P<user_id>\d+)/(?P<form_type>\w+)$', views.process_password_edits),
    url(r'^new$', views.new_user),
    url(r'^edit/(?P<user_id>\d+)$', views.edit_user),
    url(r'^edit$', views.edit_profile),
    url(r'^show/(?P<user_id>\d+)$', views.message_board),
    url(r'^create_user$', views.process_new_user),
    url(r'^edit_description$', views.edit_description),
    url(r'^create_message/(?P<user_id>\d+)$', views.create_message),
    url(r'^delete_message/(?P<user_id>\d+)$', views.delete_message),
    url(r'^create_comment/(?P<user_id>\d+)$', views.create_comment),
    url(r'^delete_comment/(?P<user_id>\d+)$', views.delete_comment),
]
