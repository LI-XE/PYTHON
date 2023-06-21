
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


def dashboard(request):
    user = None if "user_id" not in request.session else User.objects.get(
        id=request.session["user_id"])

    recent_reviews = Review.objects.order_by("-created_at")[:3]
    latest_reviewed_books = []
    for review in recent_reviews:
        latest_reviewed_books.append(Book.objects.get(id=review.book_id))

    context = {
        "user": user,
        "all_books": Book.objects.all(),
        "recent_reviews": recent_reviews,
        "latest_reviewed_books": latest_reviewed_books
    }
    return render(request, "home.html", context)


def add_book(request):
    user = None if 'user_id' not in request.session else User.objects.get(
        id=request.session['user_id'])
    if not user:
        return redirect("/login")

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
            review=request.POST["review"], rating=int(request.POST["rating"]), reviewer=user, book=book)
        book.authors.add(author)
        # messages.add_message(request, messages.SUCCESS,
        #                      "{book.title} has been added")
        print(book.__dict__)
        # print(new_review)
        return redirect(f"/books/{book.id}")
    else:
        return render(request, "addBook.html", context={"authors": Author.objects.all(), "user": user})


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


# delete review
def review_delete(request, review_id, book_id):
    user = None if 'user_id' not in request.session else User.objects.get(
        id=request.session['user_id'])
    if not user:
        return redirect("/login")

    review_to_delete = Review.objects.get(id=review_id)
    if user.id == review_to_delete.reviewer_id:
        review_to_delete.delete()
    return redirect(f"/books/{book_id}")


# User Page
def user_page(request, user_id):
    user = None if 'user_id' not in request.session else User.objects.get(
        id=request.session['user_id'])

    if not user:
        return redirect("/login")

    one_user = User.objects.get(id=user_id)
    reviews = Review.objects.filter(reviewer_id=one_user.id)
    reviewed_books = []
    for review in reviews:
        book_reviewed = Book.objects.get(id=review.book.id)
        if book_reviewed not in reviewed_books:
            reviewed_books.append(book_reviewed)

    context = {
        "user": user,
        "one_user": one_user,
        "reviews": reviews,
        "count": len(reviews),
        # or userDetail.html ---  count: {{user.reviews.all|lenghth}}
        "book_reviews": reviewed_books
    }
    return render(request, "userDetail.html", context)


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
        return render(request, "register.html", context={"user": None})


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
        return render(request, "login.html", context={"user": None})


def logout(request):
    request.session.clear()
    return redirect("/books")
