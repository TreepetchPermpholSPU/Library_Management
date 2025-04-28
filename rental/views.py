from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Rental, Member
from django.utils import timezone
from datetime import timedelta
from .models import Book
from .forms import SearchForm
from django.core.paginator import Paginator
from .forms import BookForm
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render
from .models import Rental

def book_list(request):
    form = SearchForm(request.GET)
    books = Book.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            books = books.filter(title__icontains=query)

    paginator = Paginator(books, 10) 
    page = request.GET.get('page')
    books_page = paginator.get_page(page)

    context = {
        'books': books_page,
        'form': form
    }
    return render(request, 'rental/book_list.html', context)

def rent_book(request):
    if request.method == 'POST':
        book_id = request.POST['book']
        member_id = request.POST['member']
        due_date = timezone.now().date() + timedelta(days=7)
        Rental.objects.create(
            book_id=book_id,
            member_id=member_id,
            due_date=due_date
        )
        Book.objects.filter(id=book_id).update(status='rented')
        return redirect('book_list')

    books = Book.objects.filter(status='available')
    members = Member.objects.all()
    return render(request, 'rental/rent_book.html', {'books': books, 'members': members})

def return_book(request, rental_id):
    rental = Rental.objects.get(id=rental_id)
    rental.return_date = timezone.now().date()
    overdue_days = (rental.return_date - rental.due_date).days
    rental.fine = max(0, overdue_days * 10)
    rental.book.status = 'available'
    rental.book.save()
    rental.save()
    return redirect('rental_list')

def rental_list(request):
    rentals = Rental.objects.all()

    book_query = request.GET.get('book')
    member_query = request.GET.get('member')
    rent_date_query = request.GET.get('rent_date')

    if book_query:
        rentals = rentals.filter(book__title__icontains=book_query)
    if member_query:
        rentals = rentals.filter(member__name__icontains=member_query)
    if rent_date_query:
        rentals = rentals.filter(rent_date=rent_date_query)

    rentals = rentals.order_by('-rent_date')

    return render(request, 'rental/rental_list.html', {'rentals': rentals})


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'rental/add_book.html', {'form': form})

def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'แก้ไขข้อมูลหนังสือเรียบร้อยแล้ว!')
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'rental/edit_book.html', {'form': form, 'book': book})

def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'ลบหนังสือเรียบร้อยแล้ว!')
        return redirect('book_list')
    return render(request, 'rental/confirm_delete.html', {'book': book})

