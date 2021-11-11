from random import randint

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.views.generic.base import TemplateView

from ai.users.models import Categorie, Musique, Player

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


class PlayerView(TemplateView):
    template_name = "pages/nplp.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["players"] = Player.objects.all().order_by("id")
        context["categories"] = Categorie.objects.filter(play=True).order_by("id")
        return context


def CategorieView(request, pk):
    Categorie.objects.filter(id=pk).update(activate=False)
    allMusique = Musique.objects.filter(categorie=Categorie.objects.get(id=pk))
    item_count = allMusique.count()
    if item_count:
        firstRandomNumber = randint(1, item_count - 1)
        secondRandomNumber = randint(1, item_count - 1)
        check = True
        while check:
            if firstRandomNumber == secondRandomNumber:
                firstRandomNumber = randint(1, item_count - 1)
                secondRandomNumber = randint(1, item_count - 1)
            else:
                check = False
        random_musique = [allMusique[firstRandomNumber], allMusique[secondRandomNumber]]
    else:
        random_musique = Musique.objects.filter(categorie=Categorie.objects.get(id=pk))
    context = {
        "musique": random_musique,
    }

    return render(request, "pages/details.html", context)


def CategoriesActiveView(request):
    cats = Categorie.objects.all()
    for cat in cats:
        Categorie.objects.filter(id=cat.id).update(activate=True)
    plays = Player.objects.all()
    for play in plays:
        Player.objects.filter(id=play.id).update(score=0)
    return redirect("/")


def ScoreView(request, pk, score):
    player = Player.objects.filter(id=pk)
    player.update(score=score + 10)
    return redirect("/")
