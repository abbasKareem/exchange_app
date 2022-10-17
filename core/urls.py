from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.conf.urls.i18n import i18n_patterns



admin.site.site_header = "HASSA Exchange"
admin.site.site_title = "HASSA Exchange Admin Portal"
admin.site.index_title = "Exchange مرحباً بكم في هسة"
urlpatterns = [
    # path('jet/', include('jet.urls', 'jet')),
    # path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    # path('admin_tools_stats/', include('admin_tools_stats.urls')),
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include('exchange.urls')),

]


# urlpatterns += i18n_patterns(path("admin/", admin.site.urls))