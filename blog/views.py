from django.shortcuts import render, get_object_or_404
from .models import Post, Like
from account.models import Profile
from .forms import EmailPostForm, CommentForm, PostCreateForm, PostChangeForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from slugify import slugify
from django.db.models import Q
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.decorators import login_required


def post_list(request, tag_slug=None):
    search_query = request.GET.get('search', '')

    if search_query:
        posts = Post.published.filter(Q(title__iregex=search_query) |
                                      Q(body__iregex=search_query))
        if len(posts) == 0:
            search_query = 'Не найдено'
            posts = Post.published.all()
    else:
        posts = Post.published.all()

    total_comments = Post.objects.annotate(total_comments=Count('comments'))
    total_likes = Post.objects.annotate(total_likes=Count('likes'))

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    paginator = Paginator(posts, 10)
    page_num = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_num)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    data = {'posts': posts,
            'tag': tag,
            'search_query': search_query,
            'total_comments': total_comments,
            'total_likes': total_likes}

    return render(request, 'blog/post/list.html', data)


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post/create.html'
    success_url = '/blog/'
    form_class = PostChangeForm


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post/post-delete.html'
    success_url = '/blog/'


def post_detail(request, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post)
    comments = post.comments.filter(active=True)
    form = CommentForm

    is_liked = False
    if request.user.is_authenticated:
        try:
            like = Like.objects.get(post=post, user=request.user)
            is_liked = True
        except Like.DoesNotExist:
            is_liked = False

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:5]

    data = {'post': post,
            'comments': comments,
            'form': form,
            'similar_posts': similar_posts,
            'is_liked': is_liked}

    return render(request, 'blog/post/detail.html', data)


def post_share(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{ request.user.first_name or request.user.username } рекомендует вам к прочтению '{post.title}'"
            message = f"Прочитать {post.title} можно на {post_url} ===> Коментарий: {cd['comments']}"
            send_mail(subject, message, '', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    data = {'post': post,
            'form': form,
            'sent': sent}

    return render(request, 'blog/post/share.html', data)


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()

    comment_photo = Profile.objects.get(user=comment.author)

    data = {'post': post,
            'form': form,
            'comment': comment,
            'comment_photo': comment_photo}

    return render(request, 'blog/post/comment.html', data)


def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.save()
            tags = str(request.POST['tags']).split(', ')
            post.tags.add(*tags)
    else:
        form = PostCreateForm()

    data = {'form': form}

    return render(request, 'blog/post/create.html', data)


@login_required
def post_add_like(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    like = Like.objects.filter(post=post, user=request.user)

    if like:
        like.delete()
        post.likes -= 1
        post.save()
        like_result = 0
    else:
        Like.objects.create(post=post, user=request.user)
        post.likes += 1
        post.save()
        like_result = 1

    data = {'post': post,
            'like_result': like_result}

    return render(request, 'blog/post/like.html', data)


def post_liked_list(request, tag_slug=None):

    liked_posts = Like.objects.filter(user=request.user).select_related('post')

    posts = [like.post for like in liked_posts]

    total_comments = Post.objects.annotate(total_comments=Count('comments'))
    total_likes = Post.objects.annotate(total_likes=Count('likes'))

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    paginator = Paginator(posts, 10)
    page_num = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_num)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    data = {'posts': posts,
            'tag': tag,
            'total_comments': total_comments,
            'total_likes': total_likes}

    return render(request, 'blog/post/liked_list.html', data)
