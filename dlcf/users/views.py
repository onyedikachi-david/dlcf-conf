from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, CreateView, ListView
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from dlcf.users.forms import RequestCreateForm
from dlcf.users.models import AnonymousMessage

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class RequestCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': RequestCreateForm()}
        return render(request, 'pages/home.html', context)

    def post(self, request, *args, **kwargs):
        form = RequestCreateForm(request.POST)
        if form.is_valid():
            book = form.save()
            book.save()
            return HttpResponseRedirect(reverse_lazy('request_form_sub_success'))
        return render(request, 'pages/home.html', {'form': form})


request_create_view = RequestCreateView.as_view()


def request_successful_submit(request):
    return render(request, "pages/success.html")


class PrayerRequestListView(ListView):
    model = AnonymousMessage
    template_name = "pages/prayer-request-list.html"

    def get_queryset(self, *args, **kwargs):
        qs = super(PrayerRequestListView, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-id")
        return qs

prayer_request_list_view = PrayerRequestListView.as_view()