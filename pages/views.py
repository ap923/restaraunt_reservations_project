from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from restraunts.models import Restraunt
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

class HomeListView(View):
    template_name = "home.html"
    queryset = Restraunt.objects.all()

    def get_queryset(self):
        return self.queryset

    def get(self, request, *args, **kwargs):
        context = {'object_list': self.queryset}
        return render(request, self.template_name, context)


def contact_view(request, *args, **kwargs):
    return render(request, "contact.html", {})


def about_view(request, *args, **kwargs):
    my_context = {
        "title": "This is about me",
        "my_number": 123,
        "this_is_true": True,
        "my_list": [312, 3, 4, "Abc"],
        "my_html": "<h1>hello world</h1>"
    }
    return render(request, "about.html", my_context)
