from django import forms
from django.shortcuts import render
from . import md_converter
from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)


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

def new(request):
    return render(request, "encyclopedia/new-entry.html", {
        "form": NewEntryForm()
    })

def save(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = "# " + title + "\n\n" + form.cleaned_data["content"]
            if util.get_entry(title):
                return render(request, "encyclopedia/error.html", {
                    "error_message": "An entry with this title already exists."
                })
            util.save_entry(title, content)
            return entry(request, title)
        else:
            return render(request, "encyclopedia/error.html", {
                "error_message": "Invalid form."
            })
    else:
        return render(request, "encyclopedia/error.html", {
            "error_message": "Invalid request."
        })