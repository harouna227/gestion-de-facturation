from django.urls import path

from fact.views import HomeView, AjoutCustomerView, AjoutFactureView, VisualisationFacture, get_facture_pdf


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('ajoutCustomerView/', AjoutCustomerView.as_view(), name='ajoutCustomerView'),
    path('ajoutFactureView/', AjoutFactureView.as_view(), name='ajoutFactureView'),
    path('view-facture/<int:pk>/', VisualisationFacture.as_view(), name='view_facture'),
    path('facture-pdf/<int:pk>/', get_facture_pdf, name='facture_pdf'),
]