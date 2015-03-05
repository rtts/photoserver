## Photo Server

***A simple and reliable Django photo server***

### Installation instructions

1. Install Django (`pip install django`) and clone this repository
2. Create a file named `secret_settings.py` in the django/project directory, and set the variable SECRET_KEY
3. Create a file named `debug_settings.py` in the django/project directory, and set the variable DEBUG
4. Run `./manage.py syncdb` and provide a username and password
5. Run `./manage.py makemigrations` and `./manage.py migrate` to create the database tables
6. Run `python manage.py runserver` to run the photo server locally
7. Visit http://localhost:8000/admin/ and login to start creating albums and uploading photos!

### Additional documentation

***UPDATE: The generated API documentation is now included in this repository. You can view it [here](https://rawgit.com/rtts/photoserver/master/django/static/doc/html/index.html).***

The photo server API calls are well-documented. To build the
documentation will need the [Sphinx](http://sphinx-doc.org/)
documentation builder and the
[sphinxcontrib.httpdomain](http://pythonhosted.org/sphinxcontrib-httpdomain/)
extension. Install both with the following command: `pip install
sphinx sphinxcontrib-httpdomain`. Now cd into the `doc` directory and
type `make html`. If the development server is still running, the API
documentation can now be accessed at
http://localhost:8000/static/doc/html/index.html

### Deployment

Deploying the photo server requires a secured, well monitored and
publicly accessible host. The photo server can be deployed like any
Django app. For detailed instructions, see
https://docs.djangoproject.com/en/stable/howto/deployment/ Here are
some additional considerations when deploying this (or any other)
Django app:

- In a production setting, DO NOT enable debugging. Fortunately,
  debugging is disabled by default unless explicitly enabled in
  `django/project/debug_settings.py`,

- The SQLite database is not suited for production. Edit
  `django/project/settings.py` to use a real database like
  PostgreSQL. More information can be found at
  https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DATABASES

- I am personally very fond of deploying Django apps with
  [uwsgi](http://projects.unbit.it/uwsgi) and
  [nginx](http://nginx.org/). This combination is very fast and very
  easy to configure.
