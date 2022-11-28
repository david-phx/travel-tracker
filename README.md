# CS50W Capstone Project: My 50 States

**Live demo:** [US Travel Tracker](https://travel-tracker.asatrian.com/)

**Video demo:** https://youtu.be/bz8_NLs1x_w

My capstone project for [*CS50's Web Programming with Python and JavaScript*](https://www.edx.org/course/cs50s-web-programming-with-python-and-javascript) course is a web application that helps users track their travels across the USA all the way to hitting the ultimate goal of visiting all 50 of states, while awarding them with fun achievements as they go. The idea for the app was inspired by my own bucket list item to visit every US state, and hopefully a web app like this might help me and others with a similar goal to achieve it.

## Distinctiveness and Complexity

The project draws upon the concepts, technologies, and tools from the CS50W course, but uses them to build a very different and a more complex application. It’s not a social app by its current design, although a lot of social network style functionality can be potentially added, such as followers and/or friendships between users, a like and commenting system, internal messaging, etc. Of course, it's not an ecommerce, a wiki, or a messaging app either.

The app utilizes the Django framework and Markdown2 Python library on the back end, vanilla JavaScript on the front end to make the website dynamic, to work with internal APIs, form validation, and notifications, and Bootstrap for the majority of CSS styling.

The app uses four Django models, eight URL patterns and four API routes.

The app is mobile responsive and works well on any screen size.

## Project Files and Directories

The following list describes all the files and directories of the app.

- `capstone/` - the main Django project directory
- `map/` - the application directory
    - `fixtures/` – this directory contains the initial data to import into the database
        - `achievements.json` – database data for the Achievement model
        - `states.json` – database data for the State model
    - `static/map/` - all the static content of the app
        - `flags/` - state flags in .svg format
        - `login.js` – JavaScript code to handle login and registration forms, used only in the respective views
        - `map.js` – JavaScript code to manage the interactive map, used only in the 'index' view
        - `script.js` – JavaScript code for adding trips and alerts – used in all views
        - `trips.js` – JavaScript code for editing and deleting trips – used only in the 'trips' view
        - `styles.css` – additional CSS (on top of Bootstrap) for the app
    - `templates/map/` - HTML templates for the app
        - `index.html` – index view template
        - `layout.html` – main layout template
        - `login.html` – login / register view template
        - `profile.html` – user profile template
        - `settings.html` – settings page template
        - `state.html` – state view template
        - `trips.html` – trips view template
    - `templatetags/templatetags.py` – a template tag to retain GET request parameters while navigating between pages using Django’s Paginator model
    - `admin.py`, `models.py`, `urls.py`, `views.py` – standard Django files containing the app code
- `states/` - directory containing brief information about every state in markdown (.md) format
- `README.md` - this file
- `requirements.txt` - Python packages that need to be installed in order to run the application,

## Installing and Running the Application

1. The app uses utilizes Django and Markdown2, if you don’t have them installed, you’ll need to run `pip install -r requirements.txt` command – this will take care of installing the dependencies
2. Make and apply migrations by running `python manage.py makemigrations` and `python manage.py migrate`
3. If it's a fresh database, load data for the Achievement and State models by running `python manage.py loaddata achievements.json` and `python manage.py loaddata states.json`
4. You can create a superuser by running the `python manage.py createsuperuser` command, although it’s not required
5. Run the application using `python manage.py runserver`

## API

There are four API routes used by the app to provide AJAX functionality to the user.

- `api/states` – provides a JSON list of states already visited by the current authenticated user
- `api/trip` – is used to add a new trip
- `api/trip/<int:id>` - is used to fetch information about a specific trip, and edit or delete it
- `api/username/<str:username>` - is used to asynchronously check for username availability in the registration form, so that the user can choose an available username without actually submitting the registration form. The edit username option in the settings does not use this API, and checks the username only after the form is submitted. On a live website I would have used the asynchronous username validation in the settings form too, but I wanted to use/showcase two different validation options – one using AJAX, and another with an error message in the settings view.

## Using the Application

Open the website.

A non-authenticated user will initially only see a map of the US with links to an info page for each state, a link to log in or register an account, and an inactive button to add a trip with an appropriate tooltip.

After creating a new account or logging in with an existing account (the process is very simple and self-explanatory), you’ll be presented with the full functionality of the app.

The “Add Trip” button is now active and lets you add a new trip. The location field is required, and it can be anything – a specific city, a national park, a landmark – whatever you want to call that trip. The state field is self-explanatory. The trip start and end dates, as well as the description are optional, and you can leave them empty if you choose so, however some achievements involve specific dates (or rather seasons), so you might want to fill them out.

As you start adding trips, the map will with start filling up with the states you’ve already visited (coding this part surprisingly turned out to be way easier than I anticipated).

"My Trips" link takes you to a list of all your trips, where you can look them up and filter by location, state and trip dates. By default, the list shows ten trips per page, but that number can be changed in settings.

Clicking/tapping a trip will open its description, with a flag of the respective state (clicking the flag will take you to that state’s info page), and buttons to edit or delete the trip.

Clicking your username opens a dropdown menu with your profile, settings and a link to log out.

The user profile shows the information about the user, the states they have already visited and have yet to visit (with a nice progress bar), as well as the achievements for visiting a certain number of states, certain states, or certain states in a specific season (try Alaska in the winter or Arizona in the summer 😉).

Finally, clicking "Edit Profile" button in the profile view or selecting "Settings" in the navbar takes you to the settings page, where you can change you username, your first and last names, your password, and adjust the number of displayed trips per page.

## Links and Thanks

Thank you to everyone in the CS50 team for yet another amazing course, and see you in the next one!
