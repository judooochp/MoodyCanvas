from django.shortcuts import render, get_object_or_404
from django.db import models
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.urls import reverse, path
from django.conf.urls import url
from django.template import loader
from .utils import get_height_map, get_flatness, get_grade, get_closure, get_min, get_max
from .models import Customer, Plate, Verif, Profile, Meas
import datetime

class IndexView(generic.ListView):
    template_name = 'Moody/index.html'
    context_object_name = 'recent_verifs'

    def get_queryset(self):
       return Verif.objects.order_by('-verif_date')[:15]

class CustomersView(generic.ListView):
    template_name = 'Moody/customers.html'
    context_object_name = 'customer_list'

    def get_queryset(self):
        return Customer.objects.order_by('cust_name')

class PlatesView(generic.ListView):
    template_name = 'Moody/plates.html'
    context_object_name = 'plate_list'

    def get_queryset(self):
        return Plate.objects.filter(cust_id=Customer.objects.get(cust_name=self.kwargs['custname']))

class VerifsView(generic.ListView):
    template_name = 'Moody/verifs.html'
    context_object_name = 'recent_verifs'

    def get_queryset(self):
        return Verif.objects.filter(plate_id=Plate.objects.get(plate_id=self.kwargs['id_no']))

def new_cust(request):
    template = loader.get_template('Moody/new_cust.html')
    cust = request.META.get('HTTP_HOST')
    referer = request.META.get('HTTP_REFERER')
    if referer == 'http://' + cust + '/Moody/new_cust/':
        context = { 'cust_exists': True, }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse(template.render(None, request))

def save_new_cust(request):
    custname = request.POST.get('custname')
    custname = custname.strip()
    try:
        cust = Customer.objects.get(cust_name=custname)
    except (Customer.DoesNotExist):
        cust = Customer(cust_name=custname)
        cust.save()
        return HttpResponseRedirect(reverse('Moody:plates', args=(custname,)))
    else:
        return HttpResponseRedirect(reverse('Moody:new_cust'))

def new_plate(request, custname):
    template = loader.get_template('Moody/new_plate.html')
    host = request.META.get('HTTP_HOST')
    if request.META.get('HTTP_REFERER') == 'http://' + host + '/Moody/' + custname + '/new_plate/':
        context = { 
            'cust': custname,
            'id_exists': True,
        }
    else:
        context = { 
            'cust': custname,
        }
    return HttpResponse(template.render(context, request))
    
def save_new_plate(request, custname):
    cust = Customer.objects.get(cust_name=custname)
    width = request.POST.get('plate_wid')
    length = request.POST.get('plate_len')
    #   Ensure the less-long side is saved as width.
    if width > length:
        hold = width
        width = length
        length = hold
    plate = Plate(
        cust_id=cust,
        plate_id=request.POST.get('plate_id'),
        plate_sn=request.POST.get('plate_ser'),
        plate_mfr=request.POST.get('plate_mfr'),
        plate_wid=width,
        plate_len=length,
    )
    try:
        check_id = Plate.objects.get(plate_id=plate.plate_id, cust_id=plate.cust_id)
    except (Plate.DoesNotExist):
        try:
            check_sn = Plate.objects.get(plate_sn=plate.plate_sn, plate_mfr=plate.plate_mfr)
        except (Plate.DoesNotExist):
            plate.save()
        else:
            return HttpResponseRedirect(reverse('Moody:new_plate', args=(custname,)))
    else:       #   Mfr, Width & Length are constrained by JS
            return HttpResponseRedirect(reverse('Moody:new_plate', args=(custname,)))
    return HttpResponseRedirect(reverse('Moody:plates', args=(custname,)))

class NewVerifView(generic.ListView):
    template_name = 'Moody/new_verif.html'
    context_object_name = 'plate'

    def get_queryset(self):
        return Plate.objects.get(plate_id=self.kwargs['id_no'])
    
def save_new_verif(request, custname, id_no):
    cust = Customer.objects.get(cust_name=custname)
    plate = get_object_or_404(Plate, cust_id=cust.id, plate_id=id_no)
    verif = Verif(
        plate_id = plate,
        verif_date=datetime.datetime.now(),
        verif_foot=request.POST.get('foot_len'),
        verif_north=request.POST.get('ref_line'),
        verif_NS=request.POST.get('margin_wid'),
        verif_EW=request.POST.get('margin_len'),
        verif_top=request.POST.get('top_temp'),
        verif_bot=request.POST.get('bot_temp'),
        verif_start=request.POST.get('temp_start'),
        verif_end=request.POST.get('temp_end'),
        verif_rep=request.POST.get('repeat'),
        verif_len=request.POST.get('meas_along_len'),
        verif_wid=request.POST.get('meas_along_wid'),
        verif_diag=request.POST.get('meas_along_diag'),
        verif_cert=request.POST.get('cert_no'),
        verif_tech=request.POST.get('tech_name'),
        verif_descr=request.POST.get('run_descr'),
    )
    verif_list = []  # This will save the measurements
    meas = request.POST.get('meas_total')
    for i in range(int(meas)):
        verif_list.append(request.POST.get('meas_' + str(i)))
    range_now = 0
    range_adder = int(verif.verif_diag)
    profile1_row_list = [] # These will do the calculations
    for i in range(range_adder):
        profile1_row_list.append(float(verif_list[i]))
    range_now = range_adder
    range_adder += int(verif.verif_diag)
    profile2_row_list = []
    for i in range(range_now, range_adder):
        profile2_row_list.append(float(verif_list[i]))
    range_now = range_adder
    range_adder += int(verif.verif_len)
    profile3_row_list = []
    for i in range(range_now, range_adder):
        profile3_row_list.append(float(verif_list[i]))
    range_now = range_adder
    range_adder += int(verif.verif_wid)
    profile4_row_list = []
    for i in range(range_now, range_adder):
        profile4_row_list.append(float(verif_list[i]))
    range_now = range_adder
    range_adder += int(verif.verif_len)
    profile5_row_list = []
    for i in range(range_now, range_adder):
        profile5_row_list.append(float(verif_list[i]))
    range_now = range_adder
    range_adder += int(verif.verif_wid)
    profile6_row_list = []
    for i in range(range_now, range_adder):
        profile6_row_list.append(float(verif_list[i]))
    range_now = range_adder
    range_adder += int(verif.verif_wid)
    profile7_row_list = []
    for i in range(range_now, range_adder):
        profile7_row_list.append(float(verif_list[i]))
    range_now = range_adder
    range_adder += int(verif.verif_len)
    profile8_row_list = []
    for i in range(range_now, range_adder):
        profile8_row_list.append(float(verif_list[i]))
    profiles = [
        profile1_row_list,
        profile2_row_list,
        profile3_row_list,
        profile4_row_list,
        profile5_row_list,
        profile6_row_list,
        profile7_row_list, 
        profile8_row_list,
    ]
    height_map = get_height_map(profiles, verif.verif_foot)
    verif_flatness = get_flatness(height_map)
    verif.verif_grade = get_grade(verif_flatness, verif.plate_id.plate_wid, verif.plate_id.plate_len)
    verif.verif_flat = verif_flatness
    verif.clos_7 = get_closure(profiles[6])
    verif.clos_8 = get_closure(profiles[7])
    verif.verif_min = get_min(profiles)
    verif.verif_max = get_max(profiles)
    verif.save()
    count = 0
    for meas_list in profiles:
        profile = Profile(verif_id=verif, profile_id=count)
        profile.save()
        ident = Profile.objects.get(profile_id=count, verif_id=verif)
        count2 = 0
        meass_list = list(map(float, meas_list))
        for meas in meass_list:
            measure = Meas(profile_id=ident, measurement=meas, verif_id=verif)
            measure.save()
            count2 += 1
        count += 1
    return HttpResponseRedirect(reverse('Moody:summary', args=(custname, id_no, verif.id,)))

class SummaryView(generic.ListView):
    template_name = 'Moody/summary.html'
    context_object_name = 'profile_list'

    def get_queryset(self):
        return Profile.objects.filter(verif_id=Verif.objects.get(id=self.kwargs['ver_id']))

class CanvasView(generic.ListView):
    template_name = 'Moody/map.html'
    context_object_name = 'profile_list'

    def get_queryset(self):
        return Profile.objects.filter(verif_id=Verif.objects.get(id=self.kwargs['ver_id']))

class HeightsView(generic.ListView):
    template_name = 'Moody/heights.html'
    context_object_name = 'profile_list'

    def get_queryset(self):
        return Profile.objects.filter(verif_id=Verif.objects.get(id=self.kwargs['ver_id']))