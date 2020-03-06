from django.urls import path
from .views import(
    RestrauntView,
    RestrauntListView,
    RestrauntCreateView,
    RestrauntUpdateView,
    RestrauntDeleteView,
    RestrauntReservationCreateView,
    searchRest,
    RestrauntReservationsView,

)
  

app_name = 'restraunts'
urlpatterns = [

    path('', RestrauntListView.as_view(), name = 'restraunts-list'),
    path('create/', RestrauntCreateView.as_view(), name = 'restraunts-create'),
    path('<int:id>', RestrauntView.as_view(), name = 'restraunts-detail'),
    path('<int:id>/update/', RestrauntUpdateView.as_view(), name = 'restraunts-update'),
    path('<int:id>/reserve/', RestrauntReservationCreateView.as_view(), name = 'restraunts-reserve'),
     path('<int:id>/reservations/', RestrauntReservationsView.as_view(), name = 'restraunts-reservations'),
    path('<int:id>/delete/', RestrauntDeleteView.as_view(), name = 'restraunts-delete'),
    path('search/', searchRest, name = 'searchRest'),
    
]