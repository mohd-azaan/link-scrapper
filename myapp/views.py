from django.shortcuts import render, HttpResponseRedirect
from .models import Link
from bs4 import BeautifulSoup
import requests

def scrape(request):
    if request.method == "POST":
        site = request.POST.get("site", "")
    
        page = requests.get(site)
        soup = BeautifulSoup(page.text, 'html.parser')
    
        for link in soup.find_all('a'):
            link_address = link.get('href')
            link_text = link.string
            if link_address and link_text:
                Link.objects.create(address=link_address, name=link_text)
        
        return HttpResponseRedirect('/')
    
    data = Link.objects.all()
    return render(request, 'myapp/result.html', {'data': data})

def clear(request):
    Link.objects.all().delete()
    return render(request, 'myapp/result.html')