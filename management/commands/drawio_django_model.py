from django.core.management.base import BaseCommand
from django.apps import apps
from center.settings import *
from django.db import connection

#TODO
#+ 1) перевод field в SQL типы
#+ 2) запись mxgraph
#3) layout mxgraph
#4) связи

def quotes(s):
    return "\"" + s + "\""

class MxCell(object):
    def __init__(self):
        self.id = 0
        self.parent = 1
        self.vertex = 1
        self.height = 26
        self.width = 160
        self.x = 10
        self.y = 10
        self.value = ""
        self.type = 'swimlane' # text
        self.style = {'fontStyle':'1',
                        'childLayout':'stackLayout',
                        'horizontal':'1',
                        'startSize':'26',
                        'fillColor':'#dae8fc',
                        'horizontalStack':'0',
                        'resizeParent':'1',
                        'resizeParentMax':'0',
                        'resizeLast':'0',
                        'collapsible':'1',
                        'marginBottom':'0',
                        'strokeColor':'#6c8ebf'}

    def toStr(self):
        result = "<mxCell"
        # заполнить тег из свойств ниже
        result += " id=" + quotes(str(self.id))
        result += " value=" + quotes(self.value)
        result += " parent=" + quotes(str(self.parent))
        result += (" style=\""
        + self.type + ";"
        + str(self.style).replace("{","").replace("}","").replace("'","").replace(":","=").replace(",",";") + ";\" ")
        result += "vertex=" + quotes(str(self.vertex)) + ">"
        # вложенные теги
        result += ("<mxGeometry"
                   + " x="+ quotes(str(self.x))
                   + " y=" + quotes(str(self.y))
                   + " width=" + quotes(str(self.width))
                   + " height=" + quotes(str(self.height))
                   +" as=\"geometry\"/>")
        #result += "<mxRectangle as=\"alternateBounds\"/>"
        #result += "</mxGeometry>"
        # финализация тега
        result += "</mxCell>"
        return result

class Command(BaseCommand):
    help = 'Plot class UML diagram of all models in the project'
    default_height = 26

    def handle(self, *args, **options):
        #for app_name in INSTALLED_APPS[6:-1]: # перечислить приложения
        mxfile=("<mxCell id=\"0\"/>"
        + "<mxCell id=\"1\" parent=\"0\"/>")
        mx_id = 2
        for app in apps.get_app_configs():
            print("app_name = ", app.verbose_name)
            # https://docs.djangoproject.com/en/dev/ref/applications/#django.apps.AppConfig.get_models
            # https://stackoverflow.com/questions/49457650/django-2-0-getting-all-model-list
            # https://stackoverflow.com/questions/4111244/get-a-list-of-all-installed-applications-in-django-and-their-attributes
            
            for model_i in app.get_models():
                #for model_i in apps.all_models[app_name]: # перечислить модели приложений
                print("\t\tmodel_i = ", model_i.__name__)
                parent_cell = MxCell()
                parent_cell.parent = 1
                parent_cell.id = mx_id
                parent_cell.value = model_i.__name__
                
                mx_id = parent_cell.id + 1
                n_of_fields = 0
                for field in model_i._meta.get_fields():
                    try:
                        fieldname = (field.name + ":"
                              + field.db_type(connection))
                        print("\t\t\t" + fieldname)#field.get_internal_type())
                        cell = MxCell()
                        cell.parent = parent_cell.id
                        cell.id = mx_id
                        cell.x = 0
                        cell.style = {}
                        cell.style["strokeColor"]="none";
                        cell.style["fillColor"]="none";
                        cell.style["align"]="left";
                        cell.style["verticalAlign"]="top";
                        cell.style["spacingLeft"]="4";
                        cell.style["spacingRight"]="4";
                        cell.style["overflow"]="hidden";
                        cell.style["rotatable"]="0";
                        cell.style["points"]="[[0,0.5],[1,0.5]]";
                        cell.style["portConstraint"]="eastwest";
                        cell.y = n_of_fields * 26 + 26
                        cell.value = fieldname
                        cell.type = "text"
                        mxfile += cell.toStr()
                        cell = None
                    except:
                        print("\t\t\t" + field.name + ":")
                    mx_id += 1
                    n_of_fields += 1
                parent_cell.height = n_of_fields * 26 + 26
                mxfile += parent_cell.toStr()
                parent_cell = None

        try:
            template_file = open("diagram_template.drawio","r")
            template_str = template_file.read()
            template_file.close()
            file=open("diagram.drawio","w")
            file.write(template_str.replace("{{mxcontents}}", mxfile))
            file.close()
        except:
            pass