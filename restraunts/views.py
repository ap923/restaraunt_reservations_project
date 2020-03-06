from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.views import View
from .forms import RestrauntModelForm
from .models import Restraunt, ReservationDate, TodayReservation, ReservationInterval, Seat
from reservations.views import ReservationModelForm
from reservations.models import Reservation
from django.utils import timezone
from django.db.models import Q
# BASE VIEW Class = VIEW
from django.views.generic import DetailView



def searchRest(request):
    template = 'restraunts/restraunts_list.html'
    query = request.GET.get('q') #take the item searched from the url(comes from form that user fills) so we can see if it exists in the db

    if query:
        results = Restraunt.objects.filter(Q(name__icontains=query) 
                                        | Q(cuisine__icontains=query)
                                        | Q(city__icontains=query)
                                        
                                                                    ) # icontains - returns whatever we are querying in the db
    else:
        results = Restraunt.objects.all()
    if results:
        context = {
        'results' : results
    }

    else:
        #if there are no results that meet the criteria we want to display all the restraunts
        results = Restraunt.objects.all()
        context = {
        'results' : results
    }

    return render(request,template,context)

class RestrauntReservationsView(DetailView):
    template_name = 'restraunts/restraunt_reservations.html'
   # queryset = Reservation.objects.all()    #reservations/<modelname>_list.html is the template needed

    def get(self, request, id=None, *args, **kwargs):
        id_ = self.kwargs.get("id")

        rest = Restraunt.objects.get(id = id_)
        dates = list(ReservationDate.objects.filter(restraunt = rest))
        allTimes = []
        dates_and_times = {}

        for d in dates:
            try:
                day_of_res = TodayReservation.objects.get(reservationDate = d)
            except TodayReservation.DoesNotExist:
                day_of_res = None
            
            try:
                times = list(ReservationInterval.objects.filter(day = day_of_res))
            except ReservationInterval.DoesNotExist:
                times = None

            dates_and_times[day_of_res] = times

            allTimes = allTimes + times 

        for x, y in dates_and_times.items():
            print(x, y)
        print(dates_and_times)

        context = {
            "dates" : dates,
            "allTimes" : allTimes,
            "dates_and_times": dates_and_times
            
        }
        
        return render(request, self.template_name, context)      

class RestrauntCreateView(View):
    #Staff can create a new restraunt(Unlikely going to be used much since there is one restraunt owner)
    template_name = "restraunts/restraunt_create.html"

    def get(self, request, id=None, *args, **kwargs):
        form = RestrauntModelForm()

        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, id=None, *args, **kwargs):
        #when user submits form it goes to a post request and this function catches is it and saves in the db
        form = RestrauntModelForm(request.POST)

        if form.is_valid():
            form.save()
            form = RestrauntModelForm()
        context = {"form": form}
        return render(request, self.template_name, context)


class RestrauntUpdateView(View):
    #Staff can update the restraunt information
    template_name = "restraunts/restraunt_update.html"

    def get_object(self):
        id = self.kwargs.get('id')
        obj = None
        if id is not None:
            obj = get_object_or_404(Restraunt, id=id)

        return obj

    def get(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = RestrauntModelForm(instance=obj)
            context['object'] = obj
            context['form'] = form

        return render(request, self.template_name, context)

    def post(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = RestrauntModelForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name, context)


class RestrauntListView(View):
    template_name = "restraunts/restraunts_list.html"
    queryset = Restraunt.objects.all()

    def get_queryset(self):
        return self.queryset

    def get(self, request, *args, **kwargs):
        context = {'object_list': self.queryset}
        return render(request, self.template_name, context)

class RestrauntView(View):
    template_name = "restraunts/restraunt_detail.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {}
        
        if id is not None:
            obj = get_object_or_404(Restraunt, id=id)

            context['object'] = obj
            context['rname'] = obj.name
           
        return render(request, self.template_name, context)

    def post(self, request, id=None, *args, **kwargs):
        obj = get_object_or_404(Restraunt, id=id)
        
        res = Restraunt.objects.get(pk = id)
        when_reserved = request.POST.get('when_reserved')
 
        path = str(id) + "/reserve?reserved=" + str(when_reserved) 
       
        return HttpResponseRedirect(path, when_reserved)

def replaceQuater(time):
    #replaces last 2 digits if they are 60 to 00, because hour is only 60 min 
    if(int(time[2]+time[3]) > 45):
            temp = int(time[1]) + 1
            time = time[:1] + str(temp) + '00'
    return time

def addDigit(time):
    #adds 0 to begining to conver 8am to military 0800
    if(len(time) == 3):
        time = '0' + time
    return time

def replaceHour(time):
    #makes sure that 19 45 switched to 20 00 
    if(int(time) == 11000):
        time = 2000
        print(time)
    return int(time)

def toTime(num):
    #Calls all the functions to turn a number into proper time( because when adding time intervals 14:45 + 15 = 14:60 and it should be 15:00, etc.)
    num = str(num)
    num = addDigit(num)
    num = replaceQuater(num)
    num = replaceHour(num)
    return num

def populateDay(begInt,endInt, endInterval,day_of_res, rest):
        #populates the day in db with 2 hour intervals
        #assumption is that time to eat takes 2 hours
    try:   
        interval = ReservationInterval.objects.get(day = day_of_res, timeIntervalBegin = begInt)
          
    except ReservationInterval.DoesNotExist:
        i = 0
        while(endInt < endInterval -15):
            begInt = toTime(begInt)
            endInt = toTime(endInt)

            res_time_intervals = ReservationInterval(day = day_of_res, timeIntervalBegin = begInt, timeIntervalEnd = endInt, seatsLeft = rest.seatsAvailable)
            res_time_intervals.save()
      
            begInt += 15
            endInt  +=  15
            i+=1

def updateSeats(b,e,endInterval,obj,date):
    print("res " + str(date))
    #Goes thru time intervals and if there are seats available in those intervals(2 hour window)
    #if there are seats available we decrement them by one
    #if not we want to tell the user he cannot reserve

    for i in range(8):      
        b = toTime(b)
        e = toTime(e)
                
        if(e < endInterval):
            try:
                interval = ReservationInterval.objects.get(day = date,timeIntervalBegin = b)
              
            except ReservationInterval.DoesNotExist:
                interval = None

            if  interval:
                sLeft = interval.seatsLeft -1
                if(sLeft > 0):
                    interval.seatsLeft = sLeft
                    interval.save()                
                else:
                    #TODO Don't let user make reservation if there are no seats
                    print("NO SEATS")
       
            b = b + 15
            e = e + 15
            b = toTime(b)
            e = toTime(e)
    

class RestrauntReservationCreateView(View):
    # Creates a restraunt and puts it in the database
    template_name = "restraunts/restraunt_reserve.html"
    
    def updateRestrauntDB(attr,id):
        obj = Restraunt.objects.get(pk=id)

    def get(self, request, id):
        obj = Restraunt.objects.get(pk=id)
        resDate = request.GET.get('reserved', ' ')
    
        obj = Restraunt.objects.get(pk=id)
        request.session['resDate'] = resDate
        
        print(resDate)

        d = ReservationDate(restraunt = obj, date = resDate)
        res_day = TodayReservation(reservationDate = d)

        dateExists = ReservationDate.objects.filter(date = resDate).count()
        if dateExists < 1:
            d.save()

        form = ReservationModelForm()
        context = {"form": form, "restraunt_id": id,
                   "restraunt_name": obj.name}

        return render(request, self.template_name, context)

    def post(self, request, id, *args, **kwargs):
        red = request.META['HTTP_REFERER'] #redirects to the same page
        form = ReservationModelForm(request.POST)
        
        if form.is_valid():
            dt = request.session.get('resDate')
            obj = Restraunt.objects.get(pk=id)
            #Gets the date from the get method above so we can 
           
            instance = form.save(commit=False) #dont let the form save
            instance.restraunt_reserved = obj.name
            instance.date_of_reservation = dt
            time_reserved = instance.time_of_reservation
            # we want to add field info before saving that we dont get from user input form directly
            
            form.save()
            form = ReservationModelForm()

            d = ReservationDate.objects.get(date = dt)  
            t = str(time_reserved)

            #We want to check if the date user is trying to resesve is already in the database
            # becaues if it isnt we want to create it 
            try:
                day_of_res = TodayReservation.objects.get(reservationDate = d)
                
            except TodayReservation.DoesNotExist:
                day_of_res = TodayReservation(reservationDate = d)
                day_of_res.save()
                
            resDay = day_of_res
            
            #We take the begin interval and convert it to string because it is a time attribute so we cant split it unless its a string
            bI =   str(obj.beginTime)
            eI   = str(obj.endTime) 

            #convert hh:mm to hhmm so we can do operations on it more easily
            temp = bI.split(":")
            beginInterval = int(temp[0] + temp[1])

            temp = eI.split(":")
            endInterval = int(temp[0] + temp[1])       

            begInt = int(beginInterval)
            endInt = int(beginInterval) + 15

        
            #We want to create 15 minute intervals in the database from the time the restraunt starts working to the time 
            #it finishes working. That way we can decrement seats available in a 2 hour window of the time user wants to reserve
            # for example: if a user wants to reserve at 14:15 we want to save the reservation and then decrement the seats avaiable 
            # for that time, but not only for that time because eating takes around an hour so we want to decrease the number of seats
            # from 13:15 to 15:15 in order to ensure that if someone takes a little longer to eat than expected the person after will
            # still be able to come to eat at the time reserved
            populateDay(begInt,endInt, endInterval,resDay,obj)

            temp = t.split(":")
            time = int(temp[0] + temp[1])

            b = time-100
            e = b + 15
            b = toTime(b)
            e = toTime(e)

            er = TodayReservation.objects.all()

            print(er) 
            print("b " + str(b))
            print("e " + str(e))
            
            #This is where we do the decrementing of the seats available based on the logic described above
            #(#Updates seats in time interval begining at b and ending at e without letting e get bigger than endInterval(time restraunt closes))
            updateSeats(b,e,endInterval,obj,resDay)  
            
            
            resId = Reservation.objects.latest('id')
      
            #print(resId)
            red = "../../../reservations/" + str(resId.id)
            #Once reservation is made its going to be the last one added to the db
            #so we can pull out the latest id inserted and redirect to that reservation so
            #the customer can review it
        else:
            #if the form is not valid we want to return the same page and tell the user to fill the form correctly
            pr = "Please enter a valid form"  
            context = {
                "pr" : pr,
                "form": form
            }
            return render(request, self.template_name, context)
            
        return redirect(red)

# Delete done differently for education purposes

class RestrauntObjectMixin(object):
    model = Restraunt
    lookup = 'id'

    def get_object(self):
        id = self.kwargs.get(self.lookup)
        obj = None
        if id is not None:
            obj = get_object_or_404(Restraunt, id=id)
        return obj


class RestrauntDeleteView(RestrauntObjectMixin, View):
    #Deletes restraunt from the web app as well as the db
    template_name = "restraunts/restraunt_delete.html"

    def get(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = RestrauntModelForm(instance=obj)
            context['object'] = obj
        return render(request, self.template_name, context)

    def post(self, request, id=None, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            obj.delete()
            context['object'] = None
            return redirect('/restraunts/')
        return render(request, self.template_name, context)
