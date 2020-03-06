from django.urls import path
from .views import(
    ReservationDetailView,
    ReservationListView,
    ReservationCreateView,
    ReservationUpdateView,
    ReservationDeleteView,
    ReservationConfirmationView,
    
    )

app_name = 'reservations'

urlpatterns = [
    path('', ReservationListView.as_view(), name = 'reservations-list'),
    path('<int:id>/', ReservationDetailView.as_view(), name = 'reservation-detail'), # pk(primary key)
    path('create/', ReservationCreateView.as_view(), name = 'reservation-create'),
    path('create/<int:id>', ReservationCreateView.as_view(), name = 'reservation-create'),
    path('<int:id>/update/', ReservationUpdateView.as_view(), name = 'reservation-update'),
    path('<int:id>/delete/', ReservationDeleteView.as_view(), name = 'reservation-delete'),
    path('<int:id>/confirm/', ReservationConfirmationView.as_view(), name = 'reservation-confirm'),
   

]