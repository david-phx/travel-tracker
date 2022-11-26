from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('user/<str:username>', views.profile, name='profile'),
    path('settings', views.settings, name='settings'),
    path('state/<str:state>', views.state, name='state'),
    path('trips', views.trips, name='trips'),

    # API Routes
    path('api/states', views.api_states, name='api_states'),
    path('api/trip', views.api_newtrip, name='api_newtrip'),
    path('api/trip/<int:id>', views.api_trip, name='api_trip'),
    path('api/username/<str:username>', views.api_username, name='api_username')
]
