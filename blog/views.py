from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View, ListView, DetailView, TemplateView
from .models import Blog, Author, Review
from .forms import AsideForm, ReviewForm
from django.shortcuts import render

# Create your views here.


class Feed(View):
    template_name = 'blog/feed.html'

    def get(self, request):
        author = Author.objects.first()
        return render(request, self.template_name, {"author": author, "blogs": author.blogs.all()})


class BlogList(ListView):
    template_name = 'blog/blog-list.html'
    model = Blog
    context_object_name = 'blogs'

    def get_absolute_url(self):
        return reverse('blog-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aside_form'] = AsideForm()
        return context

    def get_queryset(self):
        search_text = self.request.GET.get('search')
        if search_text is None:
            return super().get_queryset()
        return super().get_queryset().filter(name__contains=search_text)


class BlogFavourites(ListView):
    template_name = 'blog/blog-favourites.html'
    model = Blog
    context_object_name = 'blogs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aside_form'] = AsideForm()
        return context

    def post(self, request):
        blog_id = request.POST.get("id")
        saved_blogs = request.session.get('favourites')
        if saved_blogs is None:
            saved_blogs = []
            saved_blogs.append(blog_id)
        elif blog_id in saved_blogs:
            saved_blogs.remove(blog_id)
        else:
            saved_blogs.append(blog_id)

        request.session['favourites'] = saved_blogs
        request.session.save()

        return HttpResponseRedirect(reverse('blog-list'))

    def get_absolute_url(self):
        return reverse('favourites')

    def get_queryset(self):
        ids = self.request.session.get('favourites')
        search_text = self.request.GET.get('search')
        if search_text is None:
            return super().get_queryset().filter(id__in=ids)
        return super().get_queryset().filter(id__in=ids).filter(name__contains=search_text)


class Blog(DetailView):
    template_name = 'blog/blog.html'
    model = Blog
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewForm()
        return context

    def post(self, request, slug):
        form = ReviewForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            model = form.save()
            self.get_object().reviews.add(model)
            self.get_object().save()
        return HttpResponseRedirect(self.get_absolute_url())

    def get_absolute_url(self):
        return reverse('blog', kwargs={"slug": self.get_object().slug})
