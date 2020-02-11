from django.shortcuts import render, reverse
from django.views.generic import ListView,FormView
from django.views import View
from .forms import PollingUnitForm, PlainForm, PollingResultForm
from datetime import datetime
from .models import *
# Create your views here.

class HomepageView(FormView):
    template_name = 'poll/polling_unit.html'
    form_class =  PlainForm

    def get(self, request):
        """ making a get request instead of post to fetch results"""
        context = {}
        if 'pollingForm' in request.GET and len(request.GET['unit_number']) > 3:
            try:
                initial_result = PollingUnit.objects.get(polling_unit_number__iexact = request.GET['unit_number'])
                results = AnnouncedPuResults.objects.filter(polling_unit_uniqueid = initial_result.uniqueid)
                context['results'] = results.order_by('-party_score')
            except PollingUnit.DoesNotExist:
                context['results'] = None
            
        return render(request, self.template_name, context)


class ResultLGAView(FormView):
    template_name = 'poll/lga.html'
    form_class =  PlainForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lgas'] = Lga.objects.all()
        return context

    def get(self, request):
        """ making a get request instead of post to fetch results"""
        context = {'lgas':Lga.objects.all()}
        if 'lgaForm' in request.GET and int(request.GET['lga_id']) > 0:
            try:
                polling_objs = PollingUnit.objects.filter(lga_id = request.GET['lga_id'])
                results = {}
                for polling_obj in polling_objs:
                    party_results = AnnouncedPuResults.objects.filter(polling_unit_uniqueid = polling_obj.uniqueid)
                    for party_result in party_results:
                        if results.get(party_result.party_abbreviation):
                            results[party_result.party_abbreviation] +=  party_result.party_score
                        else:
                            results[party_result.party_abbreviation] =  party_result.party_score
                context['results'] = results

            except PollingUnit.DoesNotExist:
                context['results'] = None
        
        return render(request, self.template_name, context)


class PollingUnitView(FormView):
    template_name = 'poll/polling_unit_create.html';
    form_class = PlainForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parties"] = Party.objects.all()
        context['polling_units'] = PollingUnit.objects.all()
        return context
    
    def form_valid(self, form):
        if 'partyResultForm' in self.request.POST:
            form = self.get_form(PollingResultForm)
            if form.is_valid():
                print(form.cleaned_data)
                result = AnnouncedPuResults( 
                    polling_unit_uniqueid=form.cleaned_data['polling_unit'], 
                    party_abbreviation=form.cleaned_data['party_name'],
                    party_score = form.cleaned_data['party_score'],
                    date_entered=datetime.now() )

                result.save()
            else:
                print('sdfsdf')
                return super().form_invalid(form)
        else:
            print('ddsssd')
            return super().form_invalid(form)

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('create-polling-unit')
    