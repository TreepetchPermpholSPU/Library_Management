from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('rent/', views.rent_book, name='rent_book'),
    path('return/<int:rental_id>/', views.return_book, name='return_book'),
    path('rentals/', views.rental_list, name='rental_list'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
]
