# DrawioDjangoModel
Creates draw.io (mxgraph) UML class diagram from django models of django project. Represents django app which intruduce additional manage.py command, and required to be embedded into django project.

1) Deploy in django project directory.
2) Add ```'drawio_django_model'``` to ```INSTALLED_APPS = [...]```  in ```settings.py```.
3) Run ```python manage.py drawio_django_model``` from console.
4) Open ```diagram.drawio``` file in the root of django project (where manage.py is placed).

It's yet very basic instrument, creating "heap" of class blocks on the diagram for further manual layout, far from release complete. 

## Yet //TODO
1) Auto layout of diagram.
2) Add description from ```Meta.verbose_name```.
3) Add connections from ```ForeignField```.
4) Auto open diagram on complete.
5) Filename in console parameters.
6) Exception handling.
7) PNG, JPG and other file type support.
