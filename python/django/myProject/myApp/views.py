from django.shortcuts import render, redirect
from .models import Shoe

# Create your views here.


def index(request):
    return render(request, "home.html")


def new(request):
    context = {
        "all_shoes": Shoe.objects.all()
    }
    return render(request, "show.html", context)


def create(request):
    if "has_laces" not in request.POST:
        Shoe.objects.create(brand=request.POST["brand"], color=request.POST["color"],
                            material=request.POST["material"], has_laces=False, count=request.POST["count"])
    else:
        Shoe.objects.create(brand=request.POST["brand"], color=request.POST["color"],
                            material=request.POST["material"], has_laces=request.POST["has_laces"], count=request.POST["count"])

    return redirect("/new")
