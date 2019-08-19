from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, "users")
router.register(r'contacts', views.ContactViewSet, "contacts")

contact_list = views.ContactViewSet.as_view({
    'get': 'list'
})
contact_detail = views.ContactViewSet.as_view({
    'get': 'retrieve'
})

user_list = views.UserViewSet.as_view({
    'get': 'list'
})
user_detail = views.UserViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = [
    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
