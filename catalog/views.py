from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.views.generic import TemplateView

from .forms import ProductForm
from .models import Product, Category


class HomeView(TemplateView):
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Product.objects.order_by('-price')[:3]
        context['title'] = 'KUKUSHKA STORE'

        return context

    def post(self, request, *args, **kwargs):
        search = request.POST.get('search')
        print(f'Search: {search}')

        return self.get(request, *args, **kwargs)


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'КОНТАКТЫ'
        context['address'] = 'г. Санкт-Петербург,\n м. Сенная площадь,\n ул. Садовая, 54'
        context['phone'] = '+7 (812) 123-45-67'
        context['social'] = 'Telegram: @kukushka_store'

        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        search = request.POST.get('search')

        if search is not None:
            print(f'Search: {search}')
        else:
            print(f'Имя: {name}\nЭл.Почта: {email}\nТелефон:{phone}')

        return self.get(request, *args, **kwargs)


def categories(request):
    context = {
        'title': 'КАТАЛОГ',
        'object_list': Category.objects.all().order_by('name'),
    }
    return render(request, 'catalog/categories.html', context)


def get_product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    context = {
        'title': product.name,
        'object': product,
    }
    return render(request, 'catalog/product_detail.html', context)


def create_product(request):
    form = ProductForm()

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            messages.success(request, 'Товар успешно создан')
            # return JsonResponse({'product': product.name}, status=200)
        else:
            return JsonResponse({'product_error': form.errors.as_json()},
                                status=200)
        # return redirect('object_list')
    context = {
        'title': 'Создание товара',
        'form': form,
        'categories': Category.objects.all(),
    }

    return render(request, 'catalog/create_product.html', context)


def get_product_list(request):
    product_list = Product.objects.order_by('created_at')
    paginator = Paginator(product_list, 10)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'title': 'Список товаров',
        'object_list': products,
    }

    return render(request, 'catalog/product_list.html', context)
