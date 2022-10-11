from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import *
# 
from .models import *
from .forms import *


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.posts_to_home()
        context['front_page'] = Post.objects.post_to_frontpage()
        return context


class BlogView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super(BlogView, self).get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        context['front_page'] = Post.objects.post_to_frontpage()
        return context
    
    def get_queryset(self):
        kword = self.request.GET.get('kword','')
        topic = self.request.GET.get('topic','')
        query = Post.objects.search_post(kword, topic)
        return query


# DETAIL POST
def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    post_comments = post.comment_set.all().order_by('-timestamp')
    if request.user.is_authenticated:
        View.objects.get_or_create(post=post, user=request.user)

    #  Creación de un comentario
    if request.method == 'POST':
        if request.user.is_authenticated:
            Comment.objects.create(
                user=request.user,
                post=post,
                content=request.POST.get('content')
            )
            return redirect('blog:detail', slug=post.slug)

    context = {
        'post': post,
        'post_comments': post_comments,
    }
    return render(request, 'blog/detail.html', context)


# def like and dislike
@login_required
def like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like = Like.objects.filter(user=request.user, post=post)

    if like.exists():
        like[0].delete()
        return redirect('blog:detail', slug=slug)
        
    Like.objects.create(user=request.user, post=post)

    return redirect('blog:detail', slug=slug)

