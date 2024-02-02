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