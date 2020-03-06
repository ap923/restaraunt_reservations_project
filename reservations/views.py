from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect


from django.db.models import Q


from django.views.generic import(
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView
)

from .models import Reservation
from restraunts.models import Restraunt

from .forms import ReservationModelForm

# Create your views here.

def searchReservations(request):
    template = 'reservations/reservations_list.html'
    query = request.GET.get('q')

    if query:
        results = Reservation.objects.filter(Q(restraunt_reserved__icontains=query) 
                                        | Q(time_of_reservation__icontains=query)
                                        | Q(first_name__icontains=query)
                                                                    ) # icontains - returns whatever we are querying in the db
        
    else:
        results = Reservation.objects.all()

    if results:
        
        context = {
        
        'results' : results
    }

    else:
        
        context = {
        'results' : results
    }
   

    return render(request,template,context)




class ReservationListView(ListView):
   
    # reservations/<modelname>_list.html is the template needed, django takes care of it automagically
    template_name = 'reservations/reservations_list.html'

    reserved = "errr"

    def get(self, request, *args, **kwargs):
        reserved = self.request.GET.get("reserved")
        query    = self.request.GET.get("q")
        print(query)
        
        if reserved and query:
            
            queryset = Reservation.objects.filter((Q(restraunt_reserved__icontains=query) 
                                            | Q(time_of_reservation__icontains=query)
                                            | Q(first_name__icontains=query)
                                            | Q(time_of_reservation__icontains=query)), date_of_reservation__icontains = reserved)
        elif reserved:
            queryset = Reservation.objects.filter(date_of_reservation = reserved)
        elif query:
            queryset = Reservation.objects.filter(Q(restraunt_reserved__icontains=query) 
                                            | Q(time_of_reservation__icontains=query)
                                            | Q(first_name__icontains=query)
                                            | Q(time_of_reservation__icontains=query)
                                                                        )
        
                                            
        else:
            queryset = Reservation.objects.all()
                                                     
        context = {
            'object_list' : queryset
        }
        print(context)
        
        return render(request,'reservations/reservations_list.html', context)



class ReservationCreateView(CreateView):
    template_name = 'reservations/reservations_create.html'
    form_class = ReservationModelForm
    queryset = Reservation.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("name")
        return get_object_or_404(Reservation, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class ReservationConfirmationView(DetailView):
    template_name = 'reservations/reservation_confirmation.html'
    def get_object(self):
        id_ = self.kwargs.get("id")
        res = Reservation.objects.get(id = id_ )
        obj = Restraunt.objects.get(name = res.restraunt_reserved)
        obj.seatsAvailable = obj.seatsAvailable + 1
        obj.save()
        #when the staff confirms that the person reserving finished the meal we want to delete the reservation
        return redirect('/delete')
        


class ReservationDetailView(DetailView):
    template_name = 'reservations/reservations_detail.html'
   # queryset = Reservation.objects.all()    #reservations/<modelname>_list.html is the template needed

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Reservation, id=id_)

 

class ReservationUpdateView(UpdateView):
    template_name = 'reservations/reservations_create.html'
    form_class = ReservationModelForm
    queryset = Reservation.objects.all()

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Reservation, id=id_)


class ReservationDeleteView(DeleteView):
    template_name = 'reservations/reservations_delete.html'
   # queryset = Reservation.objects.all()    #reservations/<modelname>_list.html is the template needed

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Reservation, id=id_)

    def get_success_url(self):
        return reverse('reservations:reservations-list')
