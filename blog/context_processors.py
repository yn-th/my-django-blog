# blog/context_processors.py
# from .models import Category

# def categories_processor(request):
#     return {'categories': Category.objects.all()}


# blog/context_processors.py
from .models import Category, Tag

def global_context(request):
    context = {
        'categories': Category.objects.all(),
        'all_tags': Tag.objects.all(),
    }
    if request.user.is_authenticated:
        context['is_editor'] = request.user.groups.filter(name='Editors').exists() or request.user.is_superuser
        context['is_author'] = request.user.groups.filter(name='Authors').exists() or context['is_editor']
    else:
        context['is_editor'] = False
        context['is_author'] = False
    return context