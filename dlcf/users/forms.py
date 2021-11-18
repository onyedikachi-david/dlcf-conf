from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms

from dlcf.users.models import AnonymousMessage

User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


class RequestCreateForm(forms.ModelForm):
    # request = forms.CharField(required=False, widget=forms.widgets.HiddenInput())

    class Meta:
        model = AnonymousMessage
        fields = ("request",)
