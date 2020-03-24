from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from .models import *


class ObjectDetailMixin:
    """Миксин, получающий объект"""

    model = None
    template = None

    def get(self, request, slug):
        """Метод, обрабатывающий GET-запрос для получения объекта.

        На входе принимает параметры request и slug. По slug пытается получить объект из
        базы по заданному слагу. Если такой объект отсутствует - возвращает ошибку 404. Если
        объект существует - возвращает страницу с объектом.

        """

        obj = get_object_or_404(self.model, slug__iexact=slug)
        return render(request, self.template,
                      context={self.model.__name__.lower(): obj, 'admin_object': obj, 'detail': True})


class ObjectCreateMixin:
    """Миксин, создающий объект"""

    model_form = None  # задаем None в качестве значения по умолчанию для формы
    template = None  # задаем None в качестве значения по умолчанию для шаблона

    def get(self, request):
        """Метод, обрабатывающий GET-запрос при создании объекта.

        На входе принимает параметр request. Возвращает отрисованный шаблон с формой для
        создания соответствующего объекта(тега или поста).

        """

        form = self.model_form()
        return render(request, self.template, context={'form': form})

    def post(self, request):
        """Метод, обрабатывающий POST-запрос при создании объекта.

        На входе принимает параметр request. Из POST-запроса получает данные из заполненной формы.
        Осуществляет валидацию данных. В случае успеха сохраняет данные из формы и перенаправляет на
        созданный объект. В противном случае возвращает заполненную форму с указанной ошибкой.

        """

        bound_form = self.model_form(request.POST)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form})


class ObjectUpdateMixin:
    """Миксин, производящий изменения в объекте"""

    model = None
    model_form = None
    template = None

    def get(self, request, slug):
        """Метод, обрабатывающий GET-запрос при изменении объекта.

        На входе принимает параметры request и slug. По slug получает объект из базы.
        Возвращает соответствующую форму(тег или поста) с заполненными данными по заданному slug.

        """

        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(instance=obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})

    def post(self, request, slug):
        """Метод, обрабатывающий POST-запрос при обновлении объекта.

        На входе принимает параметры request и slug. По slug получает объект из базы.
        Далее заполняет форму данными, полученными из базы (из переменной obj) и от пользователя
        (полученными из POST запроса). Проводит валидацию данных. В случае успеха сохраняет изменения
        в объекте и перенаправляет на данный объект. В противном случае возвращает заполненную форму
        с указанной ошибкой.

        """

        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(request.POST, instance=obj)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})


class ObjectDeleteMixin:
    """Миксин, производящий удаление объекта"""

    model = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        """Метод, обрабатывающий GET-запрос при удалении объекта

        На входе принимает параметры request и slug. По slug получает объект из базы.
        Возвращает соответствующую форму(тег или поста) с заполненными данными по заданному slug.

        """

        obj = self.model.objects.get(slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj})

    def post(self, request, slug):
        """Метод, обрабатывающий POST-запрос при обновлении объекта.

        На входе принимает параметры request и slug. По slug получает объект из базы и удаляет
        его. Затем перенаправляет на страницу со списком объектов

        """

        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.redirect_url))
