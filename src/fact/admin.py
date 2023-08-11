from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from fact.models import *


class AdminCustomer(admin.ModelAdmin):
    list_display = ('nom', 'email', 'telephone', 'sexe', 'age', 'ville', "date_creation", 'enregistrer_par')


class AdminFacture(admin.ModelAdmin):
    list_display = ('customer', 'enregistrer_par', 'date_facture', 'dernier_update', 'paie', 'type_facture')


admin.site.register(Customer, AdminCustomer)
admin.site.register(Facture, AdminFacture)
admin.site.register(Article)


admin.site.site_title = _('Système de Gestion de Facture')
admin.site.site_header = _('Système de Gestion de Facture')
admin.site.index_title = _('Système de Gestion de Facture')

