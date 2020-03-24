from django.views.generic import View
from .models import Post, Tag
from .utils import *
from .forms import TagForm, PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q

def posts_list(request):
    """ Функция для отображения списка постов.

    На входе принимает параметр request.
    Выполняет следующие функции:
    1. отображает список все постов в блоге
    2. при указании в поисковой строке ключевого слова - отображает список постов с найденным ключевым
    словом.
    3. реализует пагинацию страниц
    Возвращает страницу со списком постов.

    """
    search_query = request.GET.get('search', '')

    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''
    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    }

    return render(request, 'blog/index.html', context=context)


class PostDetail(ObjectDetailMixin, View):
    """Класс, позволяющий получить страницу с постом.

     Наследуется от классов ObjectDetailMixin, View. От класса ObjectDetailMixin
     наследует метод get, при помощи которого по заданному слагу производится поиск
     поста в базе данных. Если такой пост отсутствует - возвращает ошибку 404. Если
     пост существует - возвращает страницу с объектом.

     """

    model = Post
    template = 'blog/post_detail.html'


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    """Класс, создающий посты в блоге.

    Наследуется от классов LoginRequiredMixin, ObjectCreateMixin, View.
    Благодаря классу LoginRequiredMixin позволяет создавать новые посты только
    авторизованным пользователям. При попытке создать пост неавторизованным пользователем
    возвращает ошибку 403 (Forbidden).
    От класса ObjectCreateMixin наследует методы get и post.
    Метод get возвращает форму для создания нового поста.
    Метод post получает данные из формы, проводит валидацию данных и в случае успеха
    сохраняет данные о новом посте в базе.

    """

    model_form = PostForm
    template = 'blog/post_create_form.html'
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    """Класс, позволяющий изменять посты в блоге.

      Наследуется от классов LoginRequiredMixin, ObjectUpdateMixin, View.
      Благодаря классу LoginRequiredMixin позволяет изменять посты только
      авторизованным пользователям. При попытке изменить пост неавторизованным пользователем
      возвращает ошибку 403 (Forbidden).
      От класса ObjectCreateMixin наследует методы get и post.
      Метод get возвращает форму для изменения поста.
      Метод post получает данные из формы, проводит валидацию данных и в случае успеха
      сохраняет измененные данные о посте в базе.

      """

    model = Post
    model_form = PostForm
    template = 'blog/post_update_form.html'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    """Класс для удаления поста.

    Наследуется от классов LoginRequiredMixin, ObjectDeleteMixin, View.
    Благодаря классу LoginRequiredMixin позволяет удалять посты только
    авторизованным пользователям. При попытке удалить пост неавторизованным пользователем
    возвращает ошибку 403 (Forbidden).
    От класса ObjectCreateMixin наследует методы get и post.
    Метод get возвращает форму с постом для удаления.
    Метод post удаляет пост из базы и перенаправляет на страницу с постами.

    """

    model = Post
    template = 'blog/post_delete_form.html'
    redirect_url = 'posts_list_url'
    raise_exception = True


class TagDetail(ObjectDetailMixin, View):
    """Класс, позволяющий получить страницу с тегом.

    Наследуется от классов ObjectDetailMixin, View. От класса ObjectDetailMixin
    наследует метод get, при помощи которого по заданному слагу производится поиск
    тега в базе данных. Если такой тег отсутствует - возвращает ошибку 404. Если
    тег существует - возвращает страницу с тегом.

    """

    model = Tag
    template = 'blog/tag_detail.html'


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    """Класс, создающий теги в блоге.

    Наследуется от классов LoginRequiredMixin, ObjectCreateMixin, View.
    Благодаря классу LoginRequiredMixin позволяет создавать новые теги только
    авторизованным пользователям. При попытке создать тег неавторизованным пользователем
    возвращает ошибку 403 (Forbidden).
    От класса ObjectCreateMixin наследует методы get и post.
    Метод get возвращает форму для создания нового тега.
    Метод post получает данные из формы, проводит валидацию данных и в случае успеха
    сохраняет данные о новом теге в базе.

    """

    model_form = TagForm
    template = 'blog/tag_create.html'
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    """Класс, позволяющий изменять информацию о теге.

    Наследуется от классов LoginRequiredMixin, ObjectUpdateMixin, View.
    Благодаря классу LoginRequiredMixin позволяет изменять информацию о теге только
    авторизованным пользователям. При попытке изменить тег неавторизованным пользователем
    возвращает ошибку 403 (Forbidden).
    От класса ObjectCreateMixin наследует методы get и post.
    Метод get возвращает форму для изменения тега. Метод post получает
    данные из формы, проводит валидацию данных и в случае успеха сохраняет измененные
    данные о теге в базе.

    """

    model = Tag
    model_form = TagForm
    template = 'blog/tag_update_form.html'
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    """Класс для удаления тега.

    Наследуется от классов LoginRequiredMixin, ObjectDeleteMixin, View.
    Благодаря классу LoginRequiredMixin позволяет удалять теги только
    авторизованным пользователям. При попытке удалить пост неавторизованным пользователем
    возвращает ошибку 403 (Forbidden).
    От класса ObjectCreateMixin наследует методы get и post.
    Метод get возвращает форму с тегом для удаления.
    Метод post удаляет тег из базы и перенаправляет на страницу с оставшимися тегами.

    """

    model = Tag
    template = 'blog/tag_delete_form.html'
    redirect_url = 'tags_list_url'
    raise_exception = True


def tags_list(request):
    """Функция для отображения списка тегов на странице

     На входе принимает параметр request. Получает все теги, имеющиеся в базе.
     Возвращает страницу со списком тегов.

     """

    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})
