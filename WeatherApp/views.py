import json
import requests

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from . import models

OW_API_KEY = "3f59299cb03f1d4beb6bd960a3f546fd"


@login_required
def index(request):
    """Home page view that displays current set of Locations with their weather information
    along with available item operations."""

    result = ""
    appStatus = ""

    if request.method == "GET":
        locations = models.Location.objects.filter(owner=request.user)
        for location in locations:
            url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'.format(location.name,
                                                                                                     OW_API_KEY)
            locationWeather = requests.get(url).json()
            if locationWeather['cod'] == 200:
                location.temperature = locationWeather['main']['temp']
                location.description = locationWeather['weather'][0]['description']
                location.icon = locationWeather['weather'][0]['icon']
                location.save()
            else:
                appStatus = "Refresh operation for {} failed. This could be an issue related with OpenWeatherMap, " \
                            "please contact with the administrator.".format(location.name)
                result = "Fail"
                break
        if result != "Fail":
            return render(request, "index.html", {"locations": locations})

    elif request.POST["submit"] == "Create":
        locationName = request.POST['locationName']
        if locationName == "":
            appStatus = "Please choose a valid location name"
            result = "Fail"
        else:
            url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'.format(locationName,
                                                                                                     OW_API_KEY)
            locationWeather = requests.get(url).json()
            if locationWeather['cod'] == 200:
                try:
                    if models.Location.objects.count() == 0:
                        newLocId = 0
                    else:
                        newLocId = models.Location.objects.latest('locID').locID + 1
                    models.Location.objects.create(locID=newLocId, name=locationWeather['name'],
                                                   temperature=locationWeather['main']['temp'],
                                                   description=locationWeather['weather'][0]['description'],
                                                   icon=locationWeather['weather'][0]['icon'], owner=request.user)
                except IntegrityError:
                    appStatus = "Please choose a location name which does not exists in your current set of " \
                                "locations."
                    result = "Fail"

            elif locationWeather['cod'] == '404' and locationWeather['message'] == 'city not found':
                appStatus = "Location could not be found, please make sure that you enter a valid location name."
                result = "Fail"
            else:
                appStatus = "Create operation failed. This could be an issue related with OpenWeatherMap, " \
                            "please contact with the administrator."
                result = "Fail"

    elif request.POST["submit"] == "Delete":
        locationName = request.POST['locationName']
        if locationName == "":
            appStatus = "Please choose a valid location name"
            result = "Fail"
        else:
            try:
                models.Location.objects.filter(owner=request.user).get(name=locationName).delete()
            except models.Location.DoesNotExist:
                appStatus = "Delete operation failed. Please make sure that location name " \
                            "exists in current set of Locations"
                result = "Fail"

    elif request.POST["submit"] == "LocationSort":
        locationName = request.POST['locationName']
        newIndex = request.POST['newIndex']
        if locationName == "":
            appStatus = "Please choose a valid Location name"
            result = "Fail"
        else:
            try:
                location = models.Location.objects.filter(owner=request.user).get(name=locationName)
                location.to(int(newIndex))
            except models.Location.DoesNotExist:
                appStatus = "Sorting operation failed. Please make sure that location name " \
                            "exists in current set of Locations"
                result = "Fail"

    elif request.POST["submit"] == "Refresh":
        try:
            locations = models.Location.objects.filter(owner=request.user)
            for location in locations:
                url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'.format(location.name,
                                                                                                         OW_API_KEY)
                locationWeather = requests.get(url).json()
                if locationWeather['cod'] == 200:
                    location.temperature = locationWeather['main']['temp']
                    location.description = locationWeather['weather'][0]['description']
                    location.icon = locationWeather['weather'][0]['icon']
                    location.save()
                else:
                    appStatus = "Refresh operation for {} failed. This could be an issue related with OpenWeatherMap, " \
                                "please contact with the administrator.".format(location.name)
                    result = "Fail"
                    break

        except models.Location.DoesNotExist:
            appStatus = "Refreshing operation failed. Please make sure that user exists" \
                        "exists in current set of Locations"
            result = "Fail"

    elif request.POST["submit"] == "Delete All":
        try:
            models.Location.objects.filter(owner=request.user).delete()
        except models.Location.DoesNotExist:
            appStatus = "Deleting all operation failed, no locations seems to exist."
            result = "Fail"

    if result == "":
        result = "Success"
    locations = models.Location.objects.filter(owner=request.user)
    return responseLocations(result, appStatus, locations)


def signup(request):
    """SignUp page view that signs up new user to the system, according to given information."""

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username, email, password)
            login(request, user)
            return redirect('index')
        except IntegrityError:
            appStatus = "Oops! It seems like this username is taken, please choose another username."
            return render(request, 'signup.html', {'status': appStatus})
    else:
        return render(request, 'signup.html')


def responseLocations(result, statusMsg, locations):
    """Helper function for returning an app request result in JSON HttpResponse"""

    locations = serializers.serialize("json", locations)
    return HttpResponse(json.dumps({'result': result, 'appStatus': statusMsg,
                                    'locations': locations}), 'text/json')

