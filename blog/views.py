from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Post, Category, Profile, Comment, User
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import Http404
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.views.generic import DeleteView
from .forms import PostForm, CommentForm, ChangForm
from django.db.models import Count

now = timezone.now()
form_date = now.strftime('%Y-%m-%d %H:%M:%S')


class Index(ListView):
    model = Post
    template_name = 'blog/index.html'
    ordering = '-pub_date'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(is_published=True,
                                   category__is_published=True,
                                   pub_date__lte=form_date).annotate(comment_count=Count('comments')).order_by('-pub_date')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    # location = 
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username})


class PostEditView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs['pk'])
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        # для автора или админа
        if obj.author == request.user or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)

        # Остальные перенаправляются, одинаково с удалением
        return redirect('blog:post_detail', pk=obj.id)
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(DeleteView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        """идентичен методу из EditComment"""
        obj = self.get_object()

        if obj.author == request.user or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)

        return redirect('blog:post_detail', pk=obj.id)

    success_url = reverse_lazy('blog:index')


class CategoryPosts(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = 10

    def get_queryset(self):

        category_slug = self.kwargs.get('category_slug')
        category = get_object_or_404(Category,
                                     slug=category_slug,
                                     is_published=True)
        post_list = Post.objects.filter(category=category,
                                        is_published=True,
                                        pub_date__lte=form_date).order_by('-pub_date').annotate(comment_count=Count('comments'))

        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        context['category'] = get_object_or_404(Category,
                                                slug=category_slug,
                                                is_published=True)
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        context['comment_count'] = self.object.comments.count()
        return context

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        # Если пост не доступен публично
        if (
            not obj.is_published
            or not obj.category.is_published
            or obj.pub_date > timezone.now()
        ):

            if not (request.user.is_authenticated and (
                request.user == obj.author or request.user.is_staff
            )):
                raise Http404()

        return super().dispatch(request, *args, **kwargs)


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comments = form.save(commit=False)
        comments.author = request.user
        comments.text = form.cleaned_data['text']
        comments.created_at = form_date
        comments.post = post
        comments.save()
    return redirect('blog:post_detail', pk=pk)


class EditComment(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return get_object_or_404(Comment, pk=self.kwargs['pk'], post=post)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        # для автора или админа
        if obj.author == request.user or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)

        # Остальные перенаправляются, одинаково с удалением
        return redirect('blog:post_detail', pk=obj.post.pk)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})


class DeleteComment(DeleteView):
    model = Comment
    template_name = 'blog/comment.html'

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return get_object_or_404(Comment, pk=self.kwargs['pk'], post=post)

    def dispatch(self, request, *args, **kwargs):
        """идентичен методу из EditComment"""
        obj = self.get_object()

        if obj.author == request.user or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)

        return redirect('blog:post_detail', pk=obj.post.pk)

    def post(self, request, *args, **kwargs):
        """
        Удаление(через POST).,
        GET не должен удалять. Это важно :<
        """
        obj = self.get_object()

        # Дополнительная защита
        if obj.author != request.user and not request.user.is_staff:
            return redirect('blog:post_detail', pk=obj.post.pk)

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})


def profile_view(request, username):
    user = get_object_or_404(User, username=username)

    # Автоматически создаём профиль, если он отсутствует
    Profile.objects.get_or_create(user=user)

    # Автор видит ВСЕ свои посты
    posts = (
        Post.objects.filter(author=user)
        .order_by('-pub_date')
        .annotate(comment_count=Count('comments'))
    )

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/profile.html',
        {
            'profile': user,
            'posts': page_obj.object_list,
            'page_obj': page_obj,
        }
    )


class EditProfile(UpdateView):
    model = Profile
    form_class = ChangForm
    template_name = 'blog/user.html'  # Шаблон для редактирования

    def get_object(self, queryset=None):
        # Получаем профиль текущего авторизованного пользователя
        user1 = get_object_or_404(User, username=self.request.user.username)
        usernames = User.objects.values_list('username', flat=True)
        if user1 not in usernames:
            return user1

    def get_success_url(self):
        # После успешного редактирования редиректим на страницу профиля
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.request.user.username}
                            )
