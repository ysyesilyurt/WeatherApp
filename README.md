# WeatherApp
WeatherApp is a simple multi-user weather application for tracking weather information of specified locations created using OpenWeatherMap API and Django. 

## Overview
Semantics behind WeatherApp is based on a system where multiple users under management of an admin, can apply CRUD operations on specified locations to get the latest weather information about them.

Users can signup to the system from ```signup``` page (which is accessible through ```login``` page) and get started to using WeatherApp directly from ```home``` page.

In ```home``` page users can display their current set locations along with their weather information as well as options for CRUD operations. Weather information that lies within the ```home``` page gets automatically updated for every 2 hours.

Get latest weather information about any city in the world with Awesome WeatherApp!!

Below there are samples from each page:

[login]: https://github.com/ysyesilyurt/WeatherApp/blob/master/images/sample_login.png 
[signup]: https://github.com/ysyesilyurt/WeatherApp/blob/master/images/sample_signup.png
[home]: https://github.com/ysyesilyurt/WeatherApp/blob/master/images/sample_home.png

```login```

![alt text][login]

```signup```

![alt text][signup]

```home```

![alt text][home]


### Fundamental Features

* CRUD operations with locations
* Drag and drop locations for prioritization purposes
* Auto refresh for weather informations of locations

## Requirements

* Django~=2.1.7
* Python 3.6+
* jQuery 
* Bootstrap (to work with provided templates)


# Installation & Usage 

Since current WeatherApp repository also contains its configured Django project (WeatherProject) you can directly clone the repository get started.

Clone the repository
```
git clone https://github.com/ysyesilyurt/WeatherApp/
```
Install requirements

```
cd WeatherApp/
pip3 install -r requirements.txt
```

Create database tables
```
./manage.py migrate
```

(Optional) Create a super user to rule other users
```
./manage.py createsuperuser
```

Run django server
```
./manage.py runserver
```
Afterwards, go to server address (if you are using your local development server just go to ```localhost:8000```) and login to the application.
If you haven't created an admin account, you can create a user account easily from  ```signup``` page. 

## Contribution

Not all cases are covered, weird bugs may appear. Feel free to open an issue if you spot a bug. 

**Have a beautiful day! :blush:**

