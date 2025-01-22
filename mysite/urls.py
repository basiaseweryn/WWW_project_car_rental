"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from account.views import register_view, logout_view, login_view, account_view, password_reset_complete_view, \
    password_reset_confirm_view, password_reset_sent_view, password_reset_request_view, rental_history_view, \
    rental_history_xml, activate_account, cancel_booking
from rental.views import search_view, results_view, book_car_view, booking_done_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', search_view, name = "search"),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name = "logout"),
    path('login/', login_view, name="login"),
    path('account/', account_view, name="account"),
    path('password-reset/', password_reset_request_view, name='password_reset'),
    path('password-reset/done/', password_reset_sent_view, name='password_reset_sent'),
    path('reset/<uidb64>/<token>/', password_reset_confirm_view, name='password_reset_confirm'),
    path('reset/done/', password_reset_complete_view, name='password_reset_complete'),
    path('search/', search_view, name = "search"),
    path('results/', results_view, name="results"),
    path('book/<int:car_id>/', book_car_view, name='book_car'),
    path('rental-history/', rental_history_view, name='rental_history'),
    path('rental-history/xml/', rental_history_xml, name='rental_history_xml'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),
    #path('booking/confirmation/<int:booking_id>/', booking_done_view, name='booking_done'),
    #path('booking-done/<int:rental_id>/', booking_done_view, name='booking_done'),
    path('book/<int:car_id>/booking-done/', booking_done_view, name='booking_done'),

    path('cancel-booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),

]







# Serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])


