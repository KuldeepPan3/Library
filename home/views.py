from django.shortcuts import render, redirect
from .models import Book, IssuedItem
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.db.models import Q
from datetime import date
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request, 'home.html')
def books(request):
    data = Book.objects.all()
    context = {"data": data}
    return render(request, "books.html", context)
def logins(request):
    # If request is post then get username and password from request
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = auth.authenticate(username=username, password=password)

        # If user is authenticated then login user
        if user is not None:
            auth.login(request, user)

            # Redirect to home page
            return redirect('/')
        else:

            # If user is not authenticated then show error message
            # and redirect to login page
            messages.info(request, 'Invalid Credential')
            return redirect('logins')
    else:

        # If request is not post then render login page
        return render(request, 'logins.html')


def registration(request):
    # If request is post then get user details from request
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check if password and confirm password matches
        if password1 == password2:

            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exist')
                return redirect('registration')

            # Check if email already exists
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already registered')
                return redirect('registration')

            # If username and email do not exist then create user
            else:

                # Create user
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                                email=email, password=password1)

                # Save user
                user.save()

                # Redirect to login page
                return redirect('logins')
        else:

            # If password and confirm password do not match then show error message
            messages.info(request, 'Password not matches')
            return redirect('registration')
    else:

        # If request is not post then render register page
        return render(request, 'registration.html')

    # Logout view to  user
def logout(request):
    # Logout user and redirect to home page
    auth.logout(request)
    return redirect('/')

    # Issue view to issue book to user
@login_required(login_url='login')
def issue(request):

    # If request is post then get book id from request
    if (request.method == 'POST'):
        book_id = request.POST['book_id']
        current_book = Book.objects.get(id=book_id)
        book = Book.objects.filter(id=book_id)
        issue_item = IssuedItem.objects.create(user_id=request.user, book_id=current_book)
        issue_item.save()
        book.update(quantity=book[0].quantity - 1)

        # Show success message and redirect to issue page
        messages.success(request, 'Book issued successfully.')

        # Get all books which are not issued to user
    my_items = IssuedItem.objects.filter(user_id=request.user, return_date__isnull=True).values_list('book_id')
    books = Book.objects.exclude(id__in=my_items).filter(quantity__gt=0)

    # Return issue page with books that are not issued to user
    return render(request, 'issue_item.html', {'books': books})
    # Return view to return book to library
@login_required(login_url='login')
def return_item(request):

        # If request is post then get book id from request
    if request.method == 'POST':
            # Get book id from request
            book_id = request.POST['book_id']
            # Get book object
            current_book = Book.objects.get(id=book_id)
            # Update book quantity
            book = Book.objects.filter(id=book_id)
            book.update(quantity=book[0].quantity + 1)

            # Update return date of book and show success message
            issue_item = IssuedItem.objects.filter(user_id=request.user, book_id=current_book, return_date__isnull=True)
            issue_item.update(return_date=date.today())
            messages.success(request, 'Book returned successfully.')

    # Get all books which are issued to user
    my_items = IssuedItem.objects.filter(user_id=request.user, return_date__isnull=True).values_list('book_id')

    # Get all books which are not issued to user
    books = Book.objects.exclude(~Q(id__in=my_items))

    # Return  page with books that are issued to user
    params = {'books': books}
    return render(request, 'return_item.html', params)
