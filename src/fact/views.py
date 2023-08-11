import datetime
import pdfkit
config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")

from django.contrib import messages
from django.db import transaction
from django.shortcuts import render
from django.views import View
from django.template.loader import get_template
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _

from fact.models import Facture, Customer, Article
from fact.utils import get_facture, pagination
from fact.decorateur import *


class HomeView(LoginRequiredSuperuserMixin, View):
    templates_name = 'index.html'
    factures = Facture.objects.select_related('customer', 'enregistrer_par').all().order_by('-date_facture')
    context = {
        'factures': factures
    }

    def get(self, request, *args, **kwargs):
        items = pagination(request, self.factures)
        self.context['factures'] = items
        
        return render(request, self.templates_name, self.context)
    

    def post(self, request, *args, **kwargs):
        
        # Modification de la facture
        if request.POST.get('id_modified'):
            paie = request.POST.get('modified')
            print(paie)
            print(type(paie))
            try:
                obj = Facture.objects.get(id=request.POST.get('id_modified'))
                if paie == 'True':
                    obj.paie = True
                else:
                    obj.paie = False
                obj.save() 
                messages.success(request, _("modifier avec succès"))
            except Exception as e:
                messages.error(request, f"Desolé, l'erreur suivante vient de {e}")        
        
        # suppression de la facture
        if request.POST.get('id_supprimer'):
            try:
                obj = Facture.objects.get(pk=request.POST.get('id_supprimer'))
                obj.delete()
                messages.success(request, _('modification éffectuée avec succès.'))
            except Exception as e:
                messages.error(request, f"Desolé, l'erreur suivante vient de {e}")
        
        #pagination
        items = pagination(request, self.factures)
        self.context['factures'] = items
        
        return render(request, self.templates_name, self.context)


class AjoutCustomerView(LoginRequiredSuperuserMixin, View):
    templates_name = 'ajouter_customer.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.templates_name)

    def post(self, request, *args, **kwargs):
        data = {
            'nom': request.POST.get('nom'),
            'email': request.POST.get('email'),
            'telephone': request.POST.get('telephone'),
            'adresse': request.POST.get('adresse'),
            'sexe': request.POST.get('sexe'),
            'age': request.POST.get('age'),
            'ville': request.POST.get('ville'),
            'code_postal': request.POST.get('code_postal'),
            'enregistrer_par': request.user
        }
        try:
            cree = Customer.objects.create(**data)
            if cree:
                messages.success(request, 'Customer bien enregistré.')
            else:
                messages.error(request, "Desolé, veuillez renvoyer les données correctes.")
        except Exception as e:
            messages.error(request, f"Desolé le système detecte ceci venant {e}.")

        return render(request, self.templates_name)


class AjoutFactureView(LoginRequiredSuperuserMixin, View):
    """ add a new invoice view """

    template_name = 'ajouter_facture.html'

    customers = Customer.objects.select_related('enregistrer_par').all()

    context = {
        'customers': customers
    }

    def get(self, request, *args, **kwargs):       
        return render(request, self.template_name, self.context)
    

    @transaction.atomic()
    def post(self, request, *args, **kwargs):

        items = []

        try:

            customer = request.POST.get('customer')

            type_facture = request.POST.get('type_facture')

            articles = request.POST.getlist('article')

            quantite = request.POST.getlist('quantite')

            prix_unitaire = request.POST.getlist('prix_unit')

            prix_total_article = request.POST.getlist('prix_total_article')

            prix_total_facture = request.POST.get('prix_total_facture')

            commentaires = request.POST.get('commmentaires')

            object_facture = {
                'customer_id': customer,
                'enregistrer_par': request.user,
                'total': prix_total_facture,
                'type_facture': type_facture,
                'commentaires': commentaires
            }

            facture = Facture.objects.create(**object_facture)

            for index, article in enumerate(articles):
                data = Article(
                    facture_id=facture.id,
                    nom_article=article,
                    quantite=quantite[index],
                    prix_unit=prix_unitaire[index],
                    prix_total=prix_total_article[index],
                )

                items.append(data)

            cree = Article.objects.bulk_create(items)

            if cree:
                messages.success(request, "Data saved successfully.")
            else:
                messages.error(request, "Sorry, please try again the sent data is corrupt.")

        except Exception as e:
            messages.error(request, f"Sorry the following error has occured {e}.")

        return render(request, self.template_name, self.context)


class VisualisationFacture(LoginRequiredSuperuserMixin, View):
    template_name = 'facture.html'
    
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        context = get_facture(pk)
                
        return render(request, self.template_name, context)
    

@superuser_required 
def get_facture_pdf(request, *args, **kwargs):
    pk = kwargs.get('pk')
    context = get_facture(pk)  
    context['date'] = datetime.datetime.today()
       
    template = get_template('facture-pdf.html')
    html = template.render(context)
    
    option = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'enable-local-file-access': ''        
    }
    # Generate pdf
     #replace with your path
    # pdfkit.from_file("filename.html", 'out.pdf', configuration=config) 
    
    pdf = pdfkit.from_string(html, False, configuration=config)
    response = HttpResponse(pdf, content_type= 'application/pdf')
    response['Content-Disposition'] = 'attachement'; filename='file_name.pdf'

    return response
        
        