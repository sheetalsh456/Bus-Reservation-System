from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core import urlresolvers
from bus.models import BusInfo
from .models import bookAticket
from bus.models import BusPickPoint, BusDropPoint

# Create your views here.
@login_required
def book_ticket(request,bus_id,template_name='bus/book_ticket_form.html'):
    page_title = 'Book a ticket'
    bus_info = get_object_or_404(BusInfo,id=bus_id)
    bus_pickup = bus_info.arriving_from
    bus_drop = bus_info.depature_at
    bus_pickuppoints = BusPickPoint.objects.filter(area=bus_pickup)
    bus_droppoints = BusDropPoint.objects.filter(area=bus_drop)
    #get all post data in postdata variable
    postdata=request.POST.copy()
    if request.method == 'POST':
        if postdata['bookticket'] == 'Book Ticket':
            #create a object for save
            bookTicket = bookAticket()
            bookTicket.email=postdata.get('email',0)
            bookTicket.phone = postdata.get('phone',0)
            bookTicket.booking_seats_num = postdata.get('noofseats',0)
            bookTicket.fare = postdata.get('fare_bus',0)
            if request.user.is_authenticated():
                bookTicket.user = request.user
            bookTicket.booking_date = postdata.get('book_date',0)
            bookTicket.bus_id = bus_id
            bookTicket.ip_address = request.META.get('REMOTE_ADDR')
            bookTicket.pickpoint_id = postdata.get('pickup_id',1)
            bookTicket.droppoint_id = postdata.get('drop_id',1)
            #save details in the table
            bookTicket.save()
            receipt_url = urlresolvers.reverse('account:my_account')
            return HttpResponseRedirect(receipt_url) 

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
    