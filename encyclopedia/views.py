from django.shortcuts import render
import markdown
from . import util
import random
from django.http import HttpResponse


from . import util
def convert_md_to_html(title):
    content=util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
         return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry(request,title):
    html_content = convert_md_to_html(title)
    if html_content == None:
        return render(request,"encyclopedia/error.html",{
            "message":"This entry does'nt exist"
        })
    else:
        return render(request,"encyclopedia/entry.html",{
            "title":title,
            "content": html_content
        })
def search(request):
        if request.method == "POST":
            entry_search = request.POST['q']
            html_content = convert_md_to_html(entry_search)
            if html_content is not None :
                return render(request,"encyclopedia/entry.html",{
            "title":entry_search,
            "content": html_content
            })
            else :
              allEntries = util.list_entries()
              reccomendation=[]
              for entry in allEntries:
                if entry_search.lower() in entry.lower():
                 reccomendation.append(entry)
              return render(request,"encyclopedia/search.html",{
                   "reccomendation" : reccomendation
              })
            
            
def new_page(request):
    if request.method == 'GET':
        return render (request,"encyclopedia/new.html")
    else:
        title= request.POST['title']
        content = request.POST['content']
        titleExist =util.get_entry(title)
        if titleExist is not None:
            return render (request,"encyclopedia/error.html",{
                "message": "Entry page already exists"
            })
        else:
            util.save_entry(title,content)
            html_content = convert_md_to_html(title)
            return render (request,"encyclopedia/entry.html",{
                "title": title,
                "content": content
            })
            
def edit(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()  

        if not title:
            return HttpResponse(f"Error: No title provided. Received POST data: {request.POST.dict()}", status=400)

        content = util.get_entry(title) or "Content not found"

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })



from django.http import HttpResponse

def save_edit(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()  
        content = request.POST.get("content", "").strip()

        print("Received Data:", request.POST.dict())  

        if not title or not content:  
            return HttpResponse(f"Error: Missing title or content. Received: {request.POST.dict()}", status=400)

        try:
            util.save_entry(title, content)  
            html_content = convert_md_to_html(title)  
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content  
            })
        except Exception as e:
            return HttpResponse(f"Error saving entry: {str(e)}", status=500)


def rand(request):
    allEntries = util.list_entries()
    rand_entry = random.choice(allEntries)
    html_content = convert_md_to_html(rand_entry)
    return render (request,"encyclopedia/entry.html",{
        "title":rand_entry,
        "content": html_content
        }
    )


