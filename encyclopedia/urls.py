from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("new-entry", views.new, name="new"),
    path("save-changes", views.save_changes, name="save_changes"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
]
