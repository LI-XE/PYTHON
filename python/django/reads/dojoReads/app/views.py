
from django.shortcuts import render, redirect
from .models import User, Book, Review, Author
from django.contrib import messages
import bcrypt


def index(request):
    user = None if "user_id" not in request.session else User.objects.get(
        id=request.session["user_id"])
    context = {
        "user": user
    }
    print(user)
    return render(request, "index.html", context)


# def new(request):
#     context = {
#         "all_shoes": Shoe.objects.all()
#     }
#     return render(request, "show.html", context)


# def create(request):
#     if "has_laces" not in request.POST:
#         Shoe.objects.create(brand=request.POST["brand"], color=request.POST["color"],
#                             material=request.POST["material"], has_laces=False, count=request.POST["count"])
#     else:
#         Shoe.objects.create(brand=request.POST["brand"], color=request.POST["color"],
#                             material=request.POST["material"], has_laces=request.POST["has_laces"], count=request.POST["count"])

#     return redirect("/new")


# # all shows
# def shows_page(request):
#     user = None if 'user_id' not in request.session else User.objects.get(
#         id=request.session['user_id'])

#     context = {
#         "all_shows": Show.objects.all(),
#         "user": user
#     }
#     print(user)
#     print(Show.objects.all().__dict__)
#     return render(request, "shows.html", context)

# # create show


def add_book(request):
    user = None if 'user_id' not in request.session else User.objects.get(
        id=request.session['user_id'])
    if not user:
        return redirect("/login")

    authors = Author.objects.all()

    if request.method == "POST":
        review_errors = Review.objects.validate(request.POST)
        book_errors = Book.objects.validate(request.POST)
        errors = list(review_errors.values()) + list(book_errors.values())

        if request.POST["author_dropdown"] == "-1":
            if request.POST["author_name"] == "":
                messages.error(
                    request, "Please either choose an author from the dropdown or create a new one.")
            else:
                author_errors = Author.objects.validate(request.POST)
                errors += list(author_errors.values())

        if errors:
            for e in errors:
                messages.error(request, e)
            return redirect("/books/add")

        if request.POST["author_dropdown"] == "-1":
            author = Author.objects.create(name=request.POST["author_name"])
        else:
            author = Author.objects.get(id=request.POST["author_dropdown"])

        book = Book.objects.create(
            title=request.POST["title"])
        review = Review.objects.create(
            review=request.POST["review"], rating=int(request.POST["rating"]), reviewer=user, book=book)
        book.authors.add(author)
        messages.add_message(request, messages.SUCCESS,
                             "{book.title} has been added")
        print(book.__dict__)
        # print(new_review)
        return redirect(f"/books/{book.id}")
    else:
        return render(request, "addBook.html", context={"authors": Author.objects.all(), "user": user})


# # edit show
# def show_edit_page(request, show_id):
#     user = None if 'user_id' not in request.session else User.objects.get(
#         id=request.session['user_id'])
#     if not user:
#         return redirect("/shows")

#     show = Show.objects.get(id=show_id)

#     if user.id != show.created_by_id:
#         return redirect("/shows")

#     print(f"ReleaseDate: {show.release_date}")
#     if request.method == "POST":
#         errors = Show.objects.validate(request.POST)

#         if errors:
#             for e in errors.values():
#                 messages.error(request, e)
#             return redirect(f"/shows/{show_id}/edit")

#         show.title = request.POST["title"]
#         show.network = request.POST["network"]
#         show.release_date = request.POST["release_date"]
#         show.description = request.POST["description"]
#         show.save()
#         print(show)
#         messages.add_message(request, messages.SUCCESS, "Show updated")

#         return redirect(f"/shows/{show_id}")

#     else:
#         return render(request, "updateShow.html", context={"show": show, "user": user})


# book detail
def book_detail(request, book_id):
    user = None if 'user_id' not in request.session else User.objects.get(
        id=request.session['user_id'])

    this_book = Book.objects.get(id=book_id)
    reviews = Review.objects.filter(book_id=this_book.id)

    # ADD Review
    if request.method == "POST":
        if not user:
            messages.error(request, "Please log in first.")

        errors = Review.objects.validate(request.POST)
        if errors:
            for e in errors.values():
                messages.error(request, e)
            return redirect(f"/books/{book_id}")

        review = Review.objects.create(review=request.POST["review"], rating=int(
            request.POST["rating"]), reviewer=user, book=this_book)

        return redirect(f"/books/{book_id}/add/review")
    else:
        context = {
            "book": this_book,
            "user": user,
            "reviews": reviews.order_by("-created_at"),
            "count": len(reviews)
        }

        return render(request, "bookDetail.html", context)


# # delete show
# def show_delete(request, show_id):
#     user = None if 'user_id' not in request.session else User.objects.get(
#         id=request.session['user_id'])
#     if not user:
#         return redirect("/shows")

#     show_to_delete = Show.objects.get(id=show_id)
#     if user.id == show_to_delete.created_by_id:
#         show_to_delete.delete()
#         messages.success(
#             request,
#             "{} by {} has been deleted".format(show_to_delete.title, show_to_delete.network))

#     return redirect("/shows")


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
            username=request.POST["username"], alios=request.POST["alios"], email=request.POST["email"], password=pw_hash)

        request.session["user_id"] = user.id

        return redirect("/books/add")
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
            return redirect("/books/add")

    else:
        return render(request, "login.html")


def logout(request):
    request.session.clear()
    return redirect("/books")
