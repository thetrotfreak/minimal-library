import uuid  # Required for unique book instances
from datetime import date

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(
        max_length=32
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=256)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey(
        'Author',
        on_delete=models.SET_NULL,
        null=True
    )
    """
    By default on_delete=models.CASCADE,
    which means that if the author was deleted,
    this book would be deleted too!
    We use SET_NULL here,
    but we could also use PROTECT or RESTRICT
    to prevent the author being deleted while any book uses it.
    """
    summary = models.TextField(
        max_length=1024
    )

    isbn = models.CharField(
        max_length=13,
        unique=True,
        verbose_name='ISBN'
    )

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(
        Genre
    )

    # language foreign key
    language = models.ForeignKey(
        'Language',
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        # e.g. .../book-detail/2
        # add proper url-to-view mapping
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4
    )

    borrower = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    book = models.ForeignKey(
        'Book',
        on_delete=models.RESTRICT,
        null=True
    )

    imprint = models.CharField(max_length=256)

    due_back = models.DateField(
        null=True,
        blank=True
    )

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m'
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    date_of_death = models.DateField(
        'Died',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'


# FIXME CharField or TextField should use '' instead of NULL
# https://stackoverflow.com/a/44272461

class Language(models.Model):
    """Model representing a language."""
    name = models.CharField(
        max_length=32
    )

    """String for representing the Model object."""

    def __str__(self):
        return self.name
