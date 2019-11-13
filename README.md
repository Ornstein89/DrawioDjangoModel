# DrawioDjangoModel
Creates draw.io (mxgraph) UML class diagram from django models of django project.
Django app, required to be embedded into django project
1) Deploy in django project directory.
2) Add ```'drawio_django_model'``` to ```INSTALLED_APPS = [...]```  in ```settings.py```.
3) Run ```python manage.py drawio_django_model``` from console.
4) Open ```diagram.drawio``` file in the root of django project (where manage.py is placed).
