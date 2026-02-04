from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
import logging
from.models import Post,about
from django.http import Http404
from django.core.paginator import Paginator
from.forms import ContactForm
from django.contrib import messages


def index(request):
    blog_var="Blog"
    posts=Post.objects.all().order_by('-id')
    paginator=Paginator(posts,5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    return render(request,"index.html",{'var':blog_var,'page_obj':page_obj})

def detail(request,slug):
   try:
    posts=Post.objects.get(slug=slug)
    related_posts=Post.objects.filter(category=posts.category).exclude(pk=posts.id)

   except Post.DoesNotExist:
    raise Http404("page does not exist")
   return render(request,"details.html",{'post':posts,'related_posts':related_posts})

    
def contact_view(request):
    logger = logging.getLogger('TESTING')

    form = ContactForm() 

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            logger.debug(
                f"POST data is {form.cleaned_data['name']}, "
                f"{form.cleaned_data['email']}, "
                f"{form.cleaned_data['message']}"
            )
            form.save()
            messages.success(request, "Form submitted successfully!")
            return redirect('blog:index')   

        else:
            logger.debug(f"Form errors are {form.errors}")
            messages.error(request, "Please correct the errors below.")
            return render(request, 'contact.html', {'form': form})
    return render(request, 'contact.html', {'form': form})
 
def about_view(request):
    about_content=about.objects.first().content   
    return render(request,'about.html',{'about_content':about_content})