
from django.shortcuts import render, redirect
from .models import Book, Review, Author
from .forms import ReviewForm, ReviewModelForm, RegisterForm, LogForm
from django.contrib.auth import logout,  authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def index(request):
    # user = None if "user_id" not in request.session else User.objects.get(
    #     id=request.session["user_id"])
    context = {
        "user": request.user
    }
    print(request.user)
    return render(request, "index.html", context)


def dashboard(request):
    # user = None if "user_id" not in request.session else User.objects.get(
    #     id=request.session["user_id"])

    recent_reviews = Review.objects.order_by("-created_at")[:3]
    latest_reviewed_books = []
    for review in recent_reviews:
        latest_reviewed_books.append(Book.objects.get(id=review.book_id))
    print(request.user)
    context = {
        "user": request.user,
        "all_books": Book.objects.all(),
        "recent_reviews": recent_reviews,
        "latest_reviewed_books": latest_reviewed_books
    }
    return render(request, "home.html", context)


@login_required
def add_book(request):
    # user = None if 'user_id' not in request.session else User.objects.get(
    #     id=request.session['user_id'])
    # if not user:
    #     return redirect("/login")

    authors = Author.objects.all()

    # if request.method == "POST" or request.method == "FILES":
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
            title=request.POST["title"], image=request.FILES["image"])
        review = Review.objects.create(
            review=request.POST["review"], rating=int(request.POST["rating"]), reviewer=request.user, book=book)
        book.authors.add(author)
        # messages.add_message(request, messages.SUCCESS,
        #                      "{book.title} has been added")
        print(book.__dict__)
        # print(new_review)
        return redirect(f"/books/{book.id}")
    else:
        return render(request, "addBook.html", context={"authors": Author.objects.all(), "user": request.user})


# book detail
@login_required
def book_detail(request, book_id):
    # user = None if 'user_id' not in request.session else User.objects.get(
    #     id=request.session['user_id'])

    this_book = Book.objects.get(id=book_id)
    reviews = Review.objects.filter(book_id=this_book.id)

    # ADD Review
    if request.method == "POST":
        if not request.user:
            messages.error(request, "Please log in first.")

        errors = Review.objects.validate(request.POST)
        if errors:
            for e in errors.values():
                messages.error(request, e)
            return redirect(f"/books/{book_id}")

        # /models.py
        # review = Review.objects.create(review=request.POST["review"], rating=int(
        #     request.POST["rating"]), reviewer=user, book=this_book)

        # /forms.py ReviewForm(forms.Form)
        # review_form = ReviewForm(request.POST)
        # print(review_form.data)

        # review = Review.objects.create(review=review_form.data["review"], rating=int(
        #     review_form.data["rating"]), reviewer=user, book=this_book)

        # /forms.py ReviewModelForm(forms.ModelForm)
        review_form = ReviewModelForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.reviewer = request.user
            review.book = this_book
            review.save()

            return redirect(f"/books/{book_id}/add/review")
        else:
            context = {
                "book": this_book,
                "user": request.user,
                "reviews": reviews.order_by("-created_at"),
                "count": len(reviews),
                "review_form": review_form}

        return render(request, "bookDetail.html", context)
    else:
        context = {
            "book": this_book,
            "user": request.user,
            "reviews": reviews.order_by("-created_at"),
            "count": len(reviews),
            # "review_form": ReviewForm(), # if /forms.py ReviewForm
            "review_form": ReviewModelForm()}

        return render(request, "bookDetail.html", context)


# delete review
@login_required
def review_delete(request, review_id, book_id):
    # user = None if 'user_id' not in request.session else User.objects.get(
    #     id=request.session['user_id'])
    # if not user:
    #     return redirect("/login")

    review_to_delete = Review.objects.get(id=review_id)
    if request.user.id == review_to_delete.reviewer_id:
        review_to_delete.delete()
    return redirect(f"/books/{book_id}")


# User Page
@login_required
def user_page(request, user_id):
    # user = None if 'user_id' not in request.session else User.objects.get(
    #     id=request.session['user_id'])

    # if not user:
    #     return redirect("/login")

    one_user = User.objects.get(id=user_id)
    reviews = Review.objects.filter(reviewer_id=one_user.id)
    reviewed_books = []
    for review in reviews:
        book_reviewed = Book.objects.get(id=review.book.id)
        if book_reviewed not in reviewed_books:
            reviewed_books.append(book_reviewed)

    context = {
        "user": request.user,
        "one_user": one_user,
        "reviews": reviews,
        "count": len(reviews),
        # or userDetail.html ---  count: {{user.reviews.all|lenghth}}
        "book_reviews": reviewed_books
    }
    return render(request, "userDetail.html", context)


def register(request):

    if request.method == "POST":
        reg_form = RegisterForm(request.POST)

        if reg_form.is_valid():
            new_user = reg_form.save()
            login(request, new_user)
            print(new_user)
            return redirect("/books")
        else:
            context = {"reg_form": reg_form}
            return render(request, "register.html", context)

        # if len(reg_form.errors) > 0:
        #     for key, value in reg_form.errors.items():
        #         messages.error(request, value)
        #     return render(request, "register.html", context={"reg_form": reg_form})

        # User.objects.create(
        #     username=request.POST["username"],
        #     email=request.POST["email"],
        #     password=request.POST["password1"],
        # )
        # return redirect("/books/add")

    else:
        return render(request, "register.html", context={"user": None, "reg_form": RegisterForm()})

# def register(request):
#     if request.method == "POST":
#         errors = User.objects.register_validator(request.POST)

#         if errors:
#             for key, value in errors.items():
#                 messages.error(request, value, extra_tags=key)
#             return redirect("/register")
#         password = request.POST["password"]
#         pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

#         user = User.objects.create(
#             username=request.POST["username"], alios=request.POST["alios"], email=request.POST["email"], password=pw_hash)

#         request.session["user_id"] = user.id

#         return redirect("/books/add")
#     else:
#         return render(request, "register.html", context={"user": None})


def login_view(request):
    if request.method == "POST":
        log_form = AuthenticationForm(data=request.POST)
        if log_form.is_valid():
            user = log_form.get_user()
            login(request, user)
        # user = authenticate(
        #     request, username=request.POST["username"], password=request.POST["password"])
        # if user is not None:
        #     login(request, user)
            return redirect("/books")
        else:
            context = {"log_form": log_form}
            print(context)
            return render(request, "login.html", context)

    else:
        return render(request, "login.html", context={"log_form": AuthenticationForm()})


# def login(request):
#     if request.method == "POST":
#         errors = User.objects.login_validator(request.POST)
#         if errors:
#             for e in errors.values():
#                 messages.error(request, e)
#             return redirect("/login")

#         else:
#             logged_user = User.objects.filter(email=request.POST["email"])[0]
#             request.session["user_id"] = logged_user.id
#             return redirect("/books/add")

#     else:
#         return render(request, "login.html", context={"user": None})


def logout_user(request):
    # request.session.clear()
    logout(request)
    return redirect("/books")
