from django.shortcuts import render

# Create your views here.

def home_page(request):
     context = {
         'Msg': 'Hello World!'
     }

     return render(request, 'clients/landing.html', context)