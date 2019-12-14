from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from webapp.models import Foto, Comments
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator


@method_decorator(ensure_csrf_cookie, name='dispatch')


class IndexView(ListView):
    model = Foto
    template_name = 'index.html'

    def get_queryset(self):
        return Foto.objects.order_by('created_at')


class FotoView(DetailView):
    model = Foto
    context_key = 'foto'
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        foto = pk
        comments = Comments.objects.filter(fotocomment=foto)
        context['comments'] = comments
        context['user'] = self.request.user
        return context


class FotoCreateView(LoginRequiredMixin, CreateView):
    model = Foto
    template_name = 'create.html'
    fields = ('foto', 'subscribe')
    # permission_required = 'webapp.add_product'
    # permission_denied_message = '403 Доступ запрещён!'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('webapp:foto_detail', kwargs={'pk': self.object.pk})


class FotoUpdateView(UpdateView):
    model = Foto
    template_name = 'update.html'
    fields = ('foto', 'subscribe', 'user')
    context_object_name = 'foto'
    # permission_required = 'webapp.change_product'
    # permission_denied_message = '403 Доступ запрещён!'

    def get_success_url(self):
        return reverse('webapp:foto_detail', kwargs={'pk': self.object.pk})


class FotoDeleteView(DeleteView):
    model = Foto
    template_name = 'delete.html'
    success_url = reverse_lazy('webapp:index')
    context_object_name = 'foto'
    # permission_required = 'webapp.delete_foto'
    # permission_denied_message = '403 Доступ запрещён!'

    def delete(self, request, *args, **kwargs):
        foto = self.object = self.get_object()
        foto.delete()
        return HttpResponseRedirect(self.get_success_url())


def login_view(request):
    context = {}
    next = request.GET.get('next')
    redirect_page = request.session.setdefault('redirect_page', next)
    if redirect_page == None:
        redirect_page = '/'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(redirect_page)
        else:
            context['has_error'] = True
    return render(request, 'login.html', context=context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('webapp:index')
# Create your views here.
