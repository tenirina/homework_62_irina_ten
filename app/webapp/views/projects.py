from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView, CreateView, DeleteView

from webapp.forms import ProjectForm, ProjectIssueForm
from webapp.models import Project, Issue


class ProjectsView(ListView):
    template_name = "projects/projects_list.html"
    model = Project
    context_object_name = 'projects'
    paginate_by = 3
    paginate_orphans = 1


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "projects/project_update.html"
    model = Project
    form_class = ProjectForm
    context_object_name = 'project'

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})


class ProjectView(DetailView):
    template_name = "projects/project.html"
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        issues = project.issue.filter(is_deleted=False)
        print(issues)
        context['issues'] = issues
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = 'projects/project_create.html'
    form_class = ProjectForm
    model = Project

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})


class ProjectIssueCreateView(LoginRequiredMixin, CreateView):
    model = Issue
    template_name = "issues/add.html"
    form_class = ProjectIssueForm

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        issue = form.save(commit=False)
        issue.project = project
        issue.save()
        return redirect("project_detail", pk=project.pk)


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "projects/conf_delete.html"
    model = Project
    success_url = reverse_lazy('projects_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        issues = project.issue.filter(is_deleted=False)
        print(issues)
        context['issues'] = issues
        return context
