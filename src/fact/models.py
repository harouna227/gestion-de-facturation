from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    """
    Nom: définition du modele personnalisé
    """
    TYPE_SEXE = (
        ("M", _("Masculin")),
        ("F", _("Feminin")),
    )
    nom = models.CharField(max_length=123)
    email = models.CharField(max_length=225)
    telephone = models.CharField(max_length=123)
    sexe = models.CharField(max_length=1, choices=TYPE_SEXE)
    age = models.CharField(max_length=12)
    adresse = models.CharField(max_length=225)
    ville = models.CharField(max_length=23)
    code_postal = models.CharField(max_length=7)
    date_creation = models.DateTimeField(auto_now_add=True)
    enregistrer_par = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Customer"

    def __str__(self):
        return self.nom


class Facture(models.Model):
    """
    nom : définition du modèle de la facture
    auteur: issifiharouna07@gmail.com
    """
    TYPE_FACTURE = (
        ('R', _('Reçu')),
        ('P', _('Facture Proforma')),
        ('F', _('Facture')),
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    enregistrer_par = models.ForeignKey(User, on_delete=models.PROTECT)
    date_facture = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=1000, decimal_places=2)
    dernier_update = models.DateTimeField(blank=True, null=True)
    paie = models.BooleanField(default=False)
    type_facture = models.CharField(max_length=1, choices=TYPE_FACTURE)
    commentaires = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        verbose_name = "Facture"

    def __str__(self):
        return f"{self.customer.nom} {self.dernier_update}"

    @property
    def get_total_facture(self):
        articles = self.article_set.all()
        prix_total_facture = sum(article.get_total_article for article in articles)


class Article(models.Model):
    """
    nom: définition du modéle article
    auteur: issifi harouna
    
    """
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    nom_article = models.CharField(max_length=50)
    quantite = models.IntegerField(default=0)
    prix_unit = models.DecimalField(max_digits=1000, decimal_places=2)
    prix_total = models.DecimalField(max_digits=1000, decimal_places=2)

    class Meta:
        verbose_name = "Articles"

    @property
    def get_total_article(self):
        prix_total_article = self.prix_unit * self.quantite





