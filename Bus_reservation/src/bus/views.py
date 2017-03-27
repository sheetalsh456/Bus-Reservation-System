from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from .models import BusInfo,BusDropArea,BusPickArea

import json
# Create your views here.
def index (request, template_name ='bus_resrv_system.html'):
    page_title = 'Bus'
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def search_bus(request,template_name ='bus/search_bus.html'):
    page_title = 'Book a ticket'
    
    if request.method == 'POST':
        post_data = request.POST.copy()
        area_from = post_data.get('area_from')
        area_from_obj = BusPickArea.objects.get(area_name=area_from)
        area_to = post_data.get('area_to')
        area_to_obj = BusDropArea.objects.get(area_name=area_to)
        print area_to_obj.id, area_from_obj.id
        bus_info_list= BusInfo.objects.filter(arriving_from=area_from_obj,depature_at=area_to_obj)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def autocomplete_pick(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        drugs = BusPickArea.objects.filter(area_name__icontains = q )[:20]
        results = []
        for drug in drugs:
            drug_json = {}
            drug_json['id'] = drug.id
            drug_json['label'] = drug.area_name
            drug_json['value'] = drug.area_name
            results.append(drug_json)
        data = json.dumps(results) 
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def autocomplete_drop(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        drugs = BusDropArea.objects.filter(area_name__icontains = q )[:20]
        results = []
        for drug in drugs:
            drug_json = {}
            drug_json['id'] = drug.id
            drug_json['label'] = drug.area_name
            drug_json['value'] = drug.area_name
            results.append(drug_json)
        data = json.dumps(results) 
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)