
from django.shortcuts import render, redirect
from .models import Shoe, Show, User
from django.contrib import messages
import bcrypt


def index(request):
    user = None if "user_id" not in request.session else User.objects.get(
        id=request.session["user_id"])
    context = {
        "user": user
    }
    print(user)
    return render(request, "home.html", context)


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


# all shows
def shows_page(request):
    user = None if 'user_id' not in request.session else User.objects.get(
        id=request.session['user_id'])

    context = {
        "all_shows": Show.objects.all(),
        "user": user
    }
    print(user)
    print(Show.objects.all().__dict__)
    return render(request, "shows.html", context)

# create show


def add_show_page(request):
    if "user_id" not in request.session:
        return redirect("/login")

    user = User.objects.get(id=request.session['user_id'])

    context = {
        "user": user
    }

    if request.method == "POST":
        errors = Show.objects.validate(request.POST)
        if errors:
            for e in errors.values():
                messages.error(request, e)
            return redirect("/shows/new")

        show = Show.objects.create(title=request.POST["title"], network=request.POST["network"],
                                   release_date=request.POST["release_date"], description=request.POST["description"], created_by=user)

        messages.add_message(request, messages.SUCCESS,
                             "{show.title} has been added")
        return redirect(f"/shows/{show.id}")
    else:
        return render(request, "createShow.html", context)


# edit show
def show_edit_page(request, show_id):
    user = None if 'user_id' not in request.session else User.objects.get(
        id=request.session['user_id'])
    if not user:
        return redirect("/shows")

    show = Show.objects.get(id=show_id)

    if user.id != show.created_by_id:
        return redirect("/shows")

    print(f"ReleaseDate: {show.release_date}")
    if request.method == "POST":
        errors = Show.objects.validate(request.POST)

        if errors:
            for e in errors.values():
                messages.error(request, e)
            return redirect(f"/shows/{show_id}/edit")

        show.title = request.POST["title"]
        show.network = request.POST["network"]
        show.release_date = request.POST["release_date"]
        show.description = request.POST["description"]
        show.save()
        print(show)
        messages.add_message(request, messages.SUCCESS, "Show updated")

        return redirect(f"/shows/{show_id}")

    else:
        return render(request, "updateShow.html", context={"show": show, "user": user})


# show detail
def show_detail(request, show_id):
    user = None if 'user_id' not in request.session else User.objects.get(
        id=request.session['user_id'])

    show = Show.objects.get(id=show_id)

    print(show_id)

    context = {
        "show": show,
        "user": user
    }
    return render(request, "showDetail.html", context)


# delete show
def show_delete(request, show_id):
    user = None if 'user_id' not in request.session else User.objects.get(
        id=request.session['user_id'])
    if not user:
        return redirect("/shows")

    show_to_delete = Show.objects.get(id=show_id)
    if user.id == show_to_delete.created_by_id:
        show_to_delete.delete()
        messages.success(
            request,
            "{} by {} has been deleted".format(show_to_delete.title, show_to_delete.network))

    return redirect("/shows")


def register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)

        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect("/register")
        password = request.POST["password"]
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        user = User.objects.create(
            username=request.POST["username"], email=request.POST["email"], password=pw_hash)

        request.session["user_id"] = user.id

        return redirect("/shows")
    else:
        return render(request, "register.html")


def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if errors:
            for e in errors.values():
                messages.error(request, e)
            return redirect("/login")

        else:
            logged_user = User.objects.filter(email=request.POST["email"])[0]
            request.session["user_id"] = logged_user.id
            return redirect("/shows")

    else:
        return render(request, "login.html")


def logout(request):
    request.session.clear()
    return redirect("/shows")
