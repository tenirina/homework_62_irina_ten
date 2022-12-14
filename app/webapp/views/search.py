from django.db.models import Q
from django.utils.http import urlencode
from django.views.generic import ListView

from webapp.forms import SearchForm
from webapp.models import Project


class SearchEngine(ListView):
    search_form = None
    search_fields = {}

    def get_query(self):
        query = Q(title__icontains=self.search_value)
        return query

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q()
            query_list = [
                Q(**{f'{key}__{value}': self.search_value})
                for key, value in self.search_fields.items()
            ]
            for query_part in query_list:
                query = (query | query_part)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return self.search_form(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search_value']
        return None


class SearchView(SearchEngine):
    template_name = 'projects/projects_list.html'
    model = Project
    context_object_name = 'projects'
    ordering = ('updated_at')
    paginate_by = 6
    search_form = SearchForm
    search_fields = {
        'title': 'icontains',
        'description': 'icontains'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'projects': Project.objects.filter(self.get_query())
                        })
        return context
