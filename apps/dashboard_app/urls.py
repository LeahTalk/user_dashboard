from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin$', views.index_admin),
    url(r'^remove/(?P<user_id>\d+)$', views.delete_user),
]
