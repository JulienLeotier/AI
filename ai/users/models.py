from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for ai."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Player(models.Model):
    name = models.CharField(_("name"), max_length=250)
    score = models.IntegerField(_("score"), default=0)
    image = models.ImageField(_("image"), upload_to="static")

    class Meta:
        verbose_name = _("player")
        verbose_name_plural = _("players")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class Musique(models.Model):
    name = models.CharField(_("name"), max_length=250)
    link = models.URLField()
    categorie = models.ForeignKey(
        "Categorie", verbose_name=_("Categories"), on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Categorie(models.Model):
    name = models.CharField(_("name"), max_length=250)
    activate = models.BooleanField(_("activate"), default=True)
    play = models.BooleanField(_("play"), default=False)

    def __str__(self):
        return self.name


class MyCategories(models.Model):
    categories = models.ManyToManyField(to=Categorie)

    def __str__(self) -> str:
        return "MyCatégories"
