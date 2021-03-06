from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.forms import ModelForm
from rideRequest.forms import RequestForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from rideRequest.models import RequestRide
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def request_ride(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RequestForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return HttpResponseRedirect(reverse('rideRequest:personalrequest'))
            #return render(request, 'driver_register_form.html', {'form': form,'registered': registered})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RequestForm()

    return render(request, 'ride_request_detail.html', {'form': form})


def personal_request(request):
    personal_ride_list = RequestRide.objects.all().filter(user=request.user)
    args = {'personal_ride_list': personal_ride_list}
    return render(request, 'user_ride_request_detail.html', args)


def driver_search(request):
    available_ride_list = RequestRide.objects.all()
    ride_dict = {'search_ride': available_ride_list}
    return render(request,'driver_search.html',ride_dict)

def delete_view(request,part_id =None):
    object = RequestRide.objects.get(id=part_id)
    object.delete()
    return HttpResponseRedirect(reverse('rideRequest:personalrequest'))

def accept_view(request,part_id =None):
    object = RequestRide.objects.get(id=part_id)
    object.status_confirm = True
    object.driver_name = request.user.username
    object.driver_vehicle_type = request.user.driver.type
    object.remaining_seat = request.user.driver.max_num_passengers - object.num_passengers
    object.save()
    subject = 'Confirmation'
    message = 'Thank you for your order'
    from_email = settings.EMAIL_HOST_USER
    to_list = [object.user.email]
    send_mail(subject, message, from_email, to_list, fail_silently=True)
    #return HttpResponse(object.remaining_seat)
    return HttpResponseRedirect(reverse('rideRequest:driversearch'))

def complete_view(request,part_id =None):
    object = RequestRide.objects.get(id=part_id)
    #return HttpResponse('hhhhhh')
    object.delete()
    return HttpResponseRedirect(reverse('rideRequest:driversearch'))

def share_view(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RequestForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            destination = form.cleaned_data['destination']
            date_time = form.cleaned_data['date_time']
            num_passengers = form.cleaned_data['num_passengers']
            type = form.cleaned_data['type']
            special_requests = form.cleaned_data['special_requests']
            share_list = RequestRide.objects.all().filter(destination=destination, date_time=date_time,
                                                        special_requests=special_requests,status_share=True)

            args = []

            if type != '4':
                share_list = share_list.filter(type=type)

            for object in share_list:
                if object.remaining_seat >= num_passengers:
                    args.append(object)
            context_dict = {'eligible_share': args,'num_passengers':num_passengers}

            return render(request,'share_ride.html',context_dict)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RequestForm()

    return render(request, 'ride_request_detail.html', {'form': form})

def join_view(request,part_id =None,num_passengers=None):
    object = RequestRide.objects.get(id=part_id)

    #if(len(RequestRide.objects.filter(join_list__contains=[request.user.username]))>0):
    #    return render(request, 'ride_request_warning.html')
    
    object.remaining_seat = object.remaining_seat - int(num_passengers)
    object.join_list.append(request.user.username)
    object.save()
    return HttpResponseRedirect(reverse('rideRequest:personalrequest'))

def edit_view(request, part_id =None):
    object = RequestRide.objects.get(id=part_id)
    if request.method == 'POST':
        form = RequestForm(request.POST)

        if form.is_valid():
            object.destination = form.cleaned_data['destination']
            object.date_time = form.cleaned_data['date_time']
            object.num_passengers = form.cleaned_data['num_passengers']
            object.type = form.cleaned_data['type']
            object.special_requests = form.cleaned_data['special_requests']
            object.status_share = form.cleaned_data['status_share']
            object.save()
            return HttpResponseRedirect(reverse('rideRequest:personalrequest'))

    else:
        default_data = {'destination': object.destination, 'date_time': object.date_time,
                        'num_passengers': object.num_passengers, 'type': object.type,
                        'special_requests': object.special_requests, 'status_share':object.status_share}
        form = RequestForm(default_data,instance=request.user)
        args = {'form': form}
        return render(request, 'ride_request_detail.html',args)


def confirmed_view(request):
    confirmed_rider_list = RequestRide.objects.all().filter(driver_name=request.user.username, status_confirm=True)
    ride_dict = {'search_ride': confirmed_rider_list}
    return render(request,'confirmed_ride.html',ride_dict)
