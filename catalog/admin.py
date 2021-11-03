from django.contrib import admin

from .models import Author, Genre, Book, BookInstance, Language

# Register your models here.

admin.site.register(Genre)


class BookInline(admin.TabularInline):
    model = Book
    extra = 0


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


# admin.site.register(Book)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

    inlines = [BookInstanceInline]


# admin.site.register(BookInstance)
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    # list view
    list_display = ('book', 'status', 'due_back', 'id')

    # detail view
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )
    # filter menu
    list_filter = ('status', 'due_back')


# admin.site.register(Author)
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')

    fields = ['first_name', 'last_name']

    inlines = [BookInline]


admin.site.register(Language)
