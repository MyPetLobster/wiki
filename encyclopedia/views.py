from django.shortcuts import render
from . import md_converter
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
    
    html_content = md_converter.md_converter(markdown_content)

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