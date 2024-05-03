from django.shortcuts import render

def frontpage (request):
    return render(request, "pdf_unlocker/frontpage.html")