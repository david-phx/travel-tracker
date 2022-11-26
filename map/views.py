import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from markdown2 import markdown

from .models import User, State, Trip, Achievement

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        trips = Trip.objects.filter(user=request.user)
    else:
        trips = None
    w_states = State.objects.filter(region='W')
    mw_states = State.objects.filter(region='MW')
    ne_states = State.objects.filter(region='NE')
    sw_states = State.objects.filter(region='SW')
    se_states = State.objects.filter(region='SE')


    return render(request, 'map/index.html', {
        "trips": trips,
        "w_states": w_states,
        "mw_states": mw_states,
        "ne_states": ne_states,
        "sw_states": sw_states,
        "se_states": se_states
    })


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']
        if password != password_confirmation:
            return render(request, 'map/login.html', {
                'message': "Passwords don't match.",
                'registration': True
            })
        try:
            user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
            user.save()
        except IntegrityError:
            return render(request, 'map/login.html', {
                'message': "Username not available.",
                'registration': True
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'map/login.html', {
            'registration': True
        })


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'map/login.html', {
                'message': "Invalid username and/or password.",
                'registration': False
            })
    else:
        return render(request, 'map/login.html', {
            'registration': False
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def profile(request, username):
    profile = User.objects.get(username=username)

    trips = Trip.objects.filter(user=profile)
    visited_states = set()
    for trip in trips:
        visited_states.add(trip.state)

    state_num = len(visited_states)
    progress = state_num / 50 * 100;

    states_to_visit = set()

    for state in State.objects.all():
        if state not in visited_states:
            states_to_visit.add(state)

    # Achievements
    achievements = set()

    if trips.count() >= 1:
        achievements.add(Achievement.objects.get(slug='first-trip'))

    if state_num >= 10:
        achievements.add(Achievement.objects.get(slug='ten-states'))

    if state_num >= 20:
        achievements.add(Achievement.objects.get(slug='twenty-states'))

    if state_num >= 30:
        achievements.add(Achievement.objects.get(slug='thirty-states'))

    if state_num >= 40:
        achievements.add(Achievement.objects.get(slug='forty-states'))

    if state_num == 50:
        achievements.add(Achievement.objects.get(slug='all-states'))

    if State.objects.get(code='HI') in visited_states:
        achievements.add(Achievement.objects.get(slug='aloha'))

    for trip in trips:
        if trip.state == State.objects.get(code='AK'):
            if trip.date1 != None:
                if trip.date1.month in [12, 1, 2, 3]:
                    achievements.add(Achievement.objects.get(slug='freezing'))
            if trip.date2 != None:
                if trip.date2.month in [12, 1, 2, 3]:
                    achievements.add(Achievement.objects.get(slug='freezing'))

        if trip.state == State.objects.get(code='AZ'):
            if trip.date1 != None:
                if trip.date1.month in [6, 7, 8, 9]:
                    achievements.add(Achievement.objects.get(slug='dry-heat'))
            if trip.date2 != None:
                if trip.date2.month in [6, 7, 8, 9]:
                    achievements.add(Achievement.objects.get(slug='dry-heat'))

    return render(request, 'map/profile.html', {
        "profile": profile,
        "visited_states": visited_states,
        "state_num": state_num,
        "states_to_visit": states_to_visit,
        "progress": progress,
        "achievements": achievements
    })


@login_required
def settings(request):
    profile = User.objects.get(pk=request.user.pk)

    if request.method == "GET":
        return render(request, 'map/settings.html', {
            "profile": profile
        })

    if request.method == "POST":
        section = request.POST["section"]

        if section == 'profile':
            # Username validation
            new_username = request.POST["username"]
            if new_username != profile.username and User.objects.filter(username=new_username).exists():
                return render(request, 'map/settings.html', {
                        "profile": profile,
                        "message": "Username not available.",
                        "message_status": 'danger'
                    })
            elif new_username != profile.username:
                profile.username = new_username

            new_email = request.POST["email"]
            new_first_name = request.POST["first_name"]
            new_last_name = request.POST["last_name"]

            profile.email = new_email
            profile.first_name = new_first_name
            profile.last_name = new_last_name

            profile.save()
            login(request, profile)

            return render(request, 'map/settings.html', {
                "profile": profile,
                "message": 'Profile updated.',
                "message_status": 'success'
            })

        elif section == 'password':
            # Passwords validation
            new_password = request.POST["new_password"]
            confirm_password = request.POST["confirm_password"]
            if new_password != '' and new_password != confirm_password:
                return render(request, 'map/settings.html', {
                    "profile": profile,
                    "message": "Passwords don't match.",
                    "message_status": 'danger'
                })
            elif new_password != '':
                profile.set_password(new_password)
                profile.save()
                login(request, profile)
                return render(request, 'map/settings.html', {
                    "profile": profile,
                    "message": 'Password updated.',
                    "message_status": 'success'
                })


        elif section == 'settings':
            trips_per_page = request.POST["trips_per_page"]
            profile.trips_per_page = int(trips_per_page)
            profile.save()

            return render(request, 'map/settings.html', {
                "profile": profile,
                "message": 'Settings updated.',
                "message_status": 'success'
            })

        else:
            return render(request, 'map/settings.html', {
                "profile": profile,
                "message": 'Bad request.',
                "message_status": 'danger'
            })


def state(request, state):
    state_obj = State.objects.get(code=state)
    if request.user.is_authenticated:
        trips = Trip.objects.filter(user=request.user, state=state_obj)
    else:
        trips = None

    try:
        f = default_storage.open(f"states/{state}.md")
        state_info = f.read().decode("utf-8")
    except FileNotFoundError:
        state_info = ''

    return render(request, 'map/state.html', {
        "state": state_obj,
        "state_info": markdown(state_info),
        "trips": trips
    })


# TODO: refresh the page or add trip if trip is added @ my trips (not index)
@login_required
def trips(request):
    profile = User.objects.get(username=request.user)
    trips = Trip.objects.filter(user=profile)
    states = State.objects.all()

    get_location = request.GET.get('loc')
    if get_location != None and get_location != '':
        trips = trips.filter(location__icontains=get_location)

    get_state = request.GET.get('state')
    if get_state != None and get_state != '':
        state_obj = State.objects.get(code=get_state)
        trips = trips.filter(state=state_obj)

    get_date1 = request.GET.get('date1')
    if get_date1 != None and get_date1 != '':
        trips = trips.filter(date1__gte=get_date1)

    get_date2 = request.GET.get('date2')
    if get_date2 != None and get_date2 != '':
        trips = trips.filter(date1__lte=get_date2)

    get_sort = request.GET.get('sort')
    if get_sort == 'asc':
        trips = trips.reverse()

    paginator = Paginator(trips, profile.trips_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'map/trips.html', {
        "profile": profile,
        "states": states,
        "get_location": get_location,
        "get_state": get_state,
        "get_date1": get_date1,
        "get_date2": get_date2,
        "get_sort": get_sort,
        "page": page
    })


# API Functions

# Return list of states current user has visited
def api_states(request):
    if request.user.is_authenticated:
        trips = Trip.objects.filter(user=request.user)
        states = set()
        for trip in trips:
            states.add(trip.state.code)
        return JsonResponse(sorted(list(states)), safe=False)
    else:
        return JsonResponse({"error": "User not logged in"}, status=400)

# Add trip
@csrf_exempt
@login_required
def api_newtrip(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    user = request.user
    data = json.loads(request.body)
    location = data.get('location')
    state = State.objects.get(code=data.get('state'))
    description = data.get('description', '')
    date1 = data.get('date1') if data.get('date1') != '' else None
    date2 = data.get('date2') if data.get('date2') != '' else None
    trip = Trip(
        user = user,
        location = location,
        state = state,
        description = description,
        date1 = date1,
        date2 = date2
    )
    trip.save()
    return JsonResponse({"message": f"Trip to {location}, {state} successfully added."}, status=201)

# Get/edit/delete trip
@csrf_exempt
@login_required
def api_trip(request, id):
    try:
        trip = Trip.objects.get(pk=id)
    except Trip.DoesNotExist:
        return JsonResponse({"error": "Trip not found."}, status=404)

    if trip.user != request.user:
        return JsonResponse({"error": "Forbiden."}, status=403)
    else:
        if request.method == "GET":
            return JsonResponse(trip.serialize(), status=200)

        if request.method == "PUT":
            data = json.loads(request.body)
            trip.location = data.get('location')
            trip.state = State.objects.get(code=data.get('state'))
            trip.description = data.get('description')
            trip.date1 = data.get('date1') if data.get('date1') != '' else None
            trip.date2 = data.get('date2') if data.get('date2') != '' else None
            trip.save()
            return JsonResponse({"message": f"Your trip to {trip.location}, {trip.state} was edited."}, status=200)

        if request.method == "DELETE":
            destination = f"{trip.location}, {trip.state}"
            trip.delete()
            return JsonResponse({"message": f"Your trip to {destination} was deleted."}, status=200)

# Check if username is available
def api_username(request, username):
    available = not User.objects.filter(username=username).exists()
    return JsonResponse({"available": available})