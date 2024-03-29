from django.shortcuts import render
from random import randint
from . import md_converter as mdc
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    markdown_content = util.get_entry(title)
    if not markdown_content:
        return render(request, "encyclopedia/error.html", {
            "error_message": "The requested page was not found."
        })
    
    html_content = mdc.md_converter(markdown_content)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })


def search(request):
    query = request.GET.get('q')
    entries = util.list_entries()
    exact_match = [entry for entry in entries if query.lower() == entry.lower()]
    if len(exact_match) == 1:
        return entry(request, exact_match[0])

    sub_matches = [entry for entry in entries if query.lower() in entry.lower()]
    
    if len(sub_matches) == 0:
        return render(request, "encyclopedia/error.html", {
            "error_message": "No results found."
        })
    
    return render(request, "encyclopedia/search.html", {
        "entries": sub_matches
    })


def new(request):
    return render(request, "encyclopedia/new.html")


def save(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = "# " + title + "\n" + request.POST.get("content")
        if title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "error_message": "The page already exists."
            })
        util.save_entry(title, content)
        return entry(request, title)
    

def edit(request, title):
    markdown_content = util.get_entry(title)
    if not markdown_content:
        return render(request, "encyclopedia/error.html", {
            "error_message": "The requested page was not found."
        })
    
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": markdown_content
    })


def save_changes(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        util.save_entry(title, content)
        return entry(request, title)
    else:
        return render(request, "encyclopedia/error.html", {
            "error_message": "Invalid request."
        })
    

def random(request):
    all_pages = util.list_entries()
    entry_count = len(all_pages)
    num = randint(0, entry_count-1)
    winner = all_pages[num]

    return entry(request, winner)


