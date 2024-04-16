from django.shortcuts import render
from django.http import HttpResponse
from .models import Contacts
from .models import TestTexts

# Create your views here.
def index(request):
    bodyHtml = TestTexts.objects.get(page_name="index")
    '''
    tom = Person.objects.get(name="Tom")    # получаем запись, где name="Tom"
bob = Person.objects.get(age=23)        # получаем запись, где age=42
people = Person.objects.all()
people = Person.objects.filter(age=23)
# использование нескольких критериев
people2 = Person.objects.filter(name="Tom", age=23)

METANIT.COM
Сайт о программировании
     
ПРОГРАММИРОВАНИЕ АССЕМБЛЕР C# JAVA WEB PYTHON C C++ SQL MONGODB GO VB.NET SWIFT KOTLIN DART PHP RUST LINUX F# НАСТРОЙКИ
Создание и получение объектов модели
Последнее обновление: 26.08.2022
    
Рассмотрим добавление в базу данных и получение из нее на примере модели Person:

1
2
3
4
5
from django.db import models
 
class Person(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()
Добавление данных
create
Для добавления данных применяется метод create():

1
tom = Person.objects.create(name="Tom", age=23)
Если добавление пройдет успешно, то объект будет иметь id, который можно получить через tom.id.

Асинхронная версия метода - acreate

1
2
3
4
5
6
7
8
9
from .models import Person
import asyncio
  
async def acreate_person():
    person = await Person.objects.acreate(name="Tim", age=26)
    print(person.name)
 
# запускаем асинхронную функцию acreate_person
asyncio.run(acreate_person())
save
Однако в своей сути метод create() использует другой метод - save(), который мы также можем использовать отдельно для добавления объекта:

1
2
tom = Person(name="Tom", age=23)
tom.save()
После успешного добавления также можно получить идентификатор добавленной записи с помощью tom.id.

bulk_create()
Метод bulk_create() (и его асинхронная версия abulk_create()) позволяет добавить набор объектов, который передается в в метод в качестве параметра:

1
2
3
4
5
6
7
8
9
from .models import Person
  
people = Person.objects.bulk_create([
    Person(name="Kate", age=24),
    Person(name="Ann", age=21),
])
 
for person in people:
    print(f"{person.id}. {person.name}")
Получение из бд
Получение одного объекта
Метод get() возвращает один объект по определенному условию, которое передается в качестве параметра:

1
2
tom = Person.objects.get(name="Tom")    # получаем запись, где name="Tom"
bob = Person.objects.get(age=23)        # получаем запись, где age=42
При использовании этого метода надо учитывать, что он предназначен для выборки таких объектов, которые имеются в единичном числе в базе данных. Если в таблице не окажется подобного объекта, то мы получим ошибку имя_модели.DoesNotExist. Если же в таблице будет несколько объектов, которые соответствуют условию, то будет сгенерированно исключение MultipleObjectsReturned. Поэтому следует применять данный метод с осторожностью, либо применять обработку соответствующих исключений:

1
2
3
4
5
6
7
8
9
10
from .models import Person
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
 
try:
    tom = Person.objects.get(name="Tom")    # MultipleObjectsReturned
    alex = Person.objects.get(name="Alex")  # ObjectDoesNotExist
except ObjectDoesNotExist:
    print("Объект не сушествует")
except MultipleObjectsReturned:
    print("Найдено более одного объекта")
Асинхронная версия метода называется aget:

1
2
3
4
5
6
7
8
9
from .models import Person
import asyncio
  
async def get_person():
    person = await Person.objects.aget(id=1)
    print(person.name)
 
# запускаем асинхронную функцию get_person
asyncio.run(get_person())
get_or_create
Метод get_or_create() (и его асинхронная версия aget_or_create) возвращает объект, а если его нет в бд, то добавляет в бд новый объект.

1
2
3
4
bob, created = Person.objects.get_or_create(name="Bob", age=24)
print(created)
print(bob.name)
print(bob.age)
В данном случае, если в таблице нет объекта со значениями name="Bob" и age=24, то он добавляется. Если есть, то он возвращается.

Метод возвращает добавленный объект (в данном случае переменная bob) и булевое значение (created), которое хранит True, если добавление прошло успешно.

Стоит учитывать, что если в таблице уже есть несколько объектов (два и больше) с указанными значениями, то сгенерируется исключение MultipleObjectsReturned.

all()
Если необходимо получить все имеющиеся объекты, то применяется метод all():

1
people = Person.objects.all()
Данный метод возвращает объект типа QuerySet.

filter()
Если надо получить все объекты, которые соответствуют определенному критерию, то применяется метод filter(), который в качестве параметра принимает критерий выборки:

1
2
3
people = Person.objects.filter(age=23)
# использование нескольких критериев
people2 = Person.objects.filter(name="Tom", age=23)
Метод filter позволяет определять более сложные условия, но поскольку это отдельная большая тем, то подробнее будет рассмотрена в отдельной статье.

exclude()
Метод exclude() позволяют исключить из выборки записи, которые соответвуют переданному в качестве параметра критерию:

1
2
# исключаем пользователей, у которых age=23
people = Person.objects.exclude(age=23)
Можно комбинировать два выше рассмотренных метода:

1
2
# выбираем всех пользователей, у которых name="Tom" кроме тех, у которых age=23
people = Person.objects.filter(name="Tom").exclude(age=23)
in_bulk()
Метод in_bulk() (и его асинхронная версия ain_bulk) является более эффективным способом для чтения большого количества записей. В качестве параметра в него можно передать список идентификаторов объектов, которые надо получить. В качестве результата он возвращает словарь, то есть объект dict:

1
2
3
4
5
6
7
8
9
10
11
# получаем все объекты
people = Person.objects.in_bulk()
for id in people:
    print(people[id].name)
    print(people[id].age)
 
# получаем объекты с id=1 и id=3
people2 = Person.objects.in_bulk([1,3])
for id in people2:
    print(people2[id].name)
    print(people2[id].age)
Метод in_bulk() возвращает словарь, где ключи представляют id объектов, а значения по этим ключам - собственно эти объекты, то есть в данном случае объекты Person.

Ограничение количества
С помощью синтаксиса списков можно получить определенную порцию данных из QuerySet:

1
2
3
from .models import Person
 
people = Person.objects.all()[:5]
В данном случае выбираем первые 5 объектов, что на уровне базы данных транслируется в SQL-выражение LIMIT 5

Первый параметр указывает, сколько объектов надо пропустить:

1
2
3
4
5
from .models import Person
 
people = Person.objects.all()[5:10]
for person in people:
    print(f"{person.id}.{person.name} - {person.age}")
В данном случае пропускаем первые 5 объектов и выбираем следующие 5 объектов до 10-го индекса, что на уровне базы данных транслируется в выражение OFFSET 5 LIMIT 5


METANIT.COM
Сайт о программировании
     
ПРОГРАММИРОВАНИЕ АССЕМБЛЕР C# JAVA WEB PYTHON C C++ SQL MONGODB GO VB.NET SWIFT KOTLIN DART PHP RUST LINUX F# НАСТРОЙКИ
Работа с формами
Отправка форм
Последнее обновление: 20.08.2022
    
Одной из форм отправки данных на сервер представляет отправка с помощью форм html, обычно в запросе типа POST. В Django в целом можно использовать два подхода для работы с формами. Во-первых, можно работать со стандартными формами html. Во-вторых, Django также предоставляет специальный функционал для работы с формами, который, возможно, в каких-то моментах упрощает работу с данными. В даннной главе рассмотрим оба подхода. А в данной статье посмотрим, как получать данные обычных форм html.

Обычно данные форм передаются на сервер в запросе типа POST. Для получения подобных данных в классе HttpRequest определено свойство POST. Например, пусть у нас есть следующий шаблон index.html:

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>METANIT.COM</title>
</head>
<body>
    <h2>User form</h2>
    <form method="post" action="postuser/">
        {% csrf_token %}
        <p>Name:<br> <input name="name" /></p>
        <p>Age:<br> <input name="age" type="number" /></p>
        <input type="submit" value="Send" />
    </form>
</body>
</html>
Здесь определена форма условно для ввода данных пользователя, которая в запросе типа POST (атрибут method="post") отправляет данные по адресу "postuser/" (атрибут action="postuser/").

На форме определены два поля ввода. Первое поле предназначено для ввода имени пользователя. Второе поле - для ввода возроста пользователя.

Также внутри формы используется тег {% csrf_token %}. Он позволяет защитить приложение от CSRF-атак, добавляя в форму в виде скрытого поля csrf-токен. Кроме того, Django по умолчанию требует наличия данного токена в получаемых данных в запросе POST.

Для отправки формы и получения ее данных определим в файле views.py следующие функции:

1
2
3
4
5
6
7
8
9
10
11
from django.shortcuts import render
from django.http import HttpResponse
 
def index(request):
    return render(request, "index.html")
 
def postuser(request):
    # получаем из данных запроса POST отправленные через форму данные
    name = request.POST.get("name", "Undefined")
    age = request.POST.get("age", 1)
    return HttpResponse(f"<h2>Name: {name}  Age: {age}</h2>")
В представлении index возвращается шаблон, который содержит форму ввода.

В представлении postuser получаем через словарь request.POST отправленные из формы данные. В этом словаре по ключу можно получить значение элемента. При этом в качестве ключей выступает названия полей форм (значения атрибутов name элементов формы):

1
<input name="age" type="number" />
Так, в данном случае название поля (значение атрибута name) равно "age". Соответственно в request.POST по этому имени мы можем получить его значение:

1
age = request.POST.get("age", 1)
Если по каким-то причинам данные с ключом "age" в запросе отсутствуют, то возвращается значени по умолчанию - 1.

Далее в файле urls.py свяжем эти функции с маршрутами:

1
2
3
4
5
6
7
from django.urls import path
from hello import views
  
urlpatterns = [
    path("", views.index),
    path("postuser/", views.postuser),
]
И после получения данных формы они отправляются обратно клиенту:

Отправка форм в веб-приложении на Django и Python
Получение массивов
Усложним задачу и добавим в форму на странице index.html несколько полей, которые будут представлять массив:

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>METANIT.COM</title>
</head>
<body>
    <h2>User form</h2>
    <form method="post" action="postuser/">
        {% csrf_token %}
        <p>Name:<br /> <input name="name" /></p>
        <p>Age:<br /> <input name="age" type="number" /></p>
        <p>
            Languages:<br />
            <input name="languages" /><br />
            <input name="languages" /><br />
            <input name="languages" /><br />
        </p>
        <input type="submit" value="Send" />
    </form>
</body>
</html>
Здесь практически та же форма, только добавлено три поля для ввода языка программирования. Причем каждое из этих полей имеет одно и то же имя - "languages". Благодаря этому при отправке формы в данных запроса будет сформирован список languages из данных, введенных в эти поля.

В файле views.py изменим функцию postuser для получения массива languages:

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
from django.shortcuts import render
from django.http import HttpResponse
 
def index(request):
    return render(request, "index.html")
 
def postuser(request):
    # получаем из строки запроса имя пользователя
    name = request.POST.get("name", "Undefined")
    age = request.POST.get("age", 1)
    langs = request.POST.getlist("languages", ["python"])
     
    return HttpResponse(f"""
                <div>Name: {name}  Age: {age}<div>
                <div>Languages: {langs}</div>
            """)
Ключевой компонент при получении списка данных из запроса представляет метод getlist(), который работает так же, как и get(), только возвращает список. Если в запросе не окажется данных с ключом languages, то возвращаем список ["python"]

Получив список, мы можем что-то сделать с его элементами, перебрать, обратиться к элементам по индексу и т.д. Но в данном случае просто передаем весь список в формируемый ответ.

Отправка массивов и списков в Django в запросе Post
Подобным образом можно передавать значения массива полей других типов, либо полей, которые представляют набор элементов, например, элемента select, который поддерживает множественный выбор:

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>METANIT.COM</title>
</head>
<body>
    <h2>User form</h2>
    <form method="post" action="postuser/">
        {% csrf_token %}
        <p>Name: <br />
            <input name="name" />
        </p>
        <p>Age: <br />
            <input name="age" type="number" />
        </p>
        <p>
            Languages:<br />
            <select multiple name="languages">
                <option>Python</option>
                <option>JavaScript</option>
                <option>C++</option>
                <option>Java</option>
             </select>
        </p>
        <input type="submit" value="Send" />
    </form>
</body>
</html>
Получение списков в Django в запросе Post

METANIT.COM
Сайт о программировании
     
ПРОГРАММИРОВАНИЕ АССЕМБЛЕР C# JAVA WEB PYTHON C C++ SQL MONGODB GO VB.NET SWIFT KOTLIN DART PHP RUST LINUX F# НАСТРОЙКИ
Статические файлы
Последнее обновление: 16.08.2022
    
Веб-приложение, как правило, использует различные статические файлы - изображения, файлы стилей css, скриптов javascript и так далее. Рассмотрим, как мы можем использовать подобые файлы.

При создании проекта Django он уже имеет некоторую базовую настройку для работы со статическими файлами. В частности, в файле settings.py определена переменная STATIC_URL, которая хранит путь к каталогу со статическими файлами:

1
STATIC_URL = 'static/'
А среди установленных приложений в переменной INSTALLED_APPS указано приложение django.contrib.staticfiles

1
2
3
4
5
6
7
8
9
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hello',
]
Настройка статических файлов в файле settings.py в проекте на Django
Переменная STATIC_URL имеет значение "static/", а это значит, что нам достаточно создать в папке приложения каталог с именем "static" и добавить в него необходимые нам статические файлы. Но, естественно, при необходимости через данную настройку мы можем изменить расположение каталога статических файлов.

Итак, добавим в папку приложения новый каталог static. Чтобы не сваливать все статические файлы в кучу, определим для каждого типа файлов отдельные папки. В частности, создадим в папке static для изображений каталог images, а для стилей - каталог css. Подобным образом можно создавать папки и для других типов файлов.

В папку static/images добавим какое-нибудь изображение - в моем случае это будет файл forest.jpg. А в папке static/css определим новый файл styles.css, который будет иметь какие-нибудь простейшие стили, например:

1
2
3
body{ font-family: Verdana;}
h1{color:navy;}
img{width:350px;}
Статчиеские файлы в проекте на Django
Теперь используем эти файлы в шаблоне. Для этого в начале файла шаблона необходимо определить инструкцию

1
{% load static %}
При этом данный код должен идти после тега DOCTYPE.

Для определения пути к статическим файлам используются выражения типа

1
{% static "путь к файлу внутри папки static" %}
Так, пусть в приложении в папке templates определен шаблон index.html, который имеет следующий код:

1
2
3
4
5
6
7
8
9
10
11
12
13
<!DOCTYPE html>
{% load static %}
<html>
<head>
    <meta charset="utf-8" />
    <link rel="stylesheet" href="{% static "css/styles.css" %}" />
    <title>Django на METANIT.COM</title>
</head>
<body>
    <h1>Зимний лес</h1>
    <img src="{% static "images/forest.jpg" %}" alt="зимний лес" >
</body>
</html>
Работа со статическими файлами в веб-приложении на Django
При запуске приложения шаблон index.html будет генерироваться в следующую веб-страницу, которая будет использовать изображение и применять стили:

подключение статических файлов в приложении на Django и Python
Настройка путей к файлам
Если нас не устраивает хранение файлов в каталоге по умолчанию - каталоге static, либо мы хотим указать несколько папок, то мы можем в файле settings.py задать все необходимые каталоги с помощью переменной STATICFILES_DIRS, которая принимает список путей:

1
2
3
4
5
STATICFILES_DIRS = [
    BASE_DIR / "static",
    "/var/www/static/",
    "/somefolder/"
]

METANIT.COM
Сайт о программировании
     
ПРОГРАММИРОВАНИЕ АССЕМБЛЕР C# JAVA WEB PYTHON C C++ SQL MONGODB GO VB.NET SWIFT KOTLIN DART PHP RUST LINUX F# НАСТРОЙКИ
Шаблоны
Создание и использование шаблонов
Последнее обновление: 16.08.2022
    
Шаблоны (templates) отвечают за формирование внешнего вида приложения. Они предоставляют специальный синтаксис, который позволяет внедрять данные в код HTML.

Допустим, у нас есть проект metanit, и в нем определено одно приложение - hello:

Шаблоны Templates в Django
Настройка функциональности шаблонов в проекте Django производится в файле settings.py. с помощью переменной TEMPLATES. Так, по умолчанию переменная TEMPLATES в файле settings.py имеет следующее определение:

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
Данная переменная принимает список конфигураций для каждого движка шаблонов. По умолчанию определена одна конфигурация, которая имеет следующшие параметры

BACKEND: движок шаблонов. По умолчанию применяется встроенный движок django.template.backends.django.DjangoTemplates

DIRS: определяет список каталогов, где движок шаблонов будет искать файлы шаблонов. По умолчанию пустой список

APP_DIRS: указывает, будет ли движок шаблонов искать шаблоны внутри папок приложений в папке templates.

OPTIONS: определяет дополнительный список параметров

Итак, в конфигурации по умолчанию параметр APP_DIRS имеет значение True, а это значит, что движок шаблонов будет также искать нужные файлы шаблонов в папке приложения в каталоге templates. То есть по умолчанию мы уже имеем настроенную конфигурацию, готовую к использованию шаблонов. Теперь определим сами шаблоны.

Добавим в папку приложения каталог templates. А в нем определим файл index.html:

Добавление шаблонов Templates в проект на Django и Python
Далее в файле index.html определим следующий код:

1
2
3
4
5
6
7
8
9
10
<!DOCTYPE html>
<html>
<head>
    <title>Django на METANIT.COM</title>
    <meta charset="utf-8" />
</head>
<body>
    <h2>Hello METANIT.COM</h2>
</body>
</html>
По сути это обычная веб-страница, которая содержит код html. Теперь используем эту страницу для отправки ответа пользователю. И для этого перейдем в приложении hello к файлу views.py, который определяет функции для обработки запроса. Изменим этот файл следующим образом:

1
2
3
4
from django.shortcuts import render
 
def index(request):
    return render(request, "index.html")
Из модуля django.shortcuts импортируется функция render.

Функция index вызывает функцию render, которой передаются объект запроса request и путь к файлу шаблона в рамках папки templates - "index.html".

В файле urls.py проекта пропишем сопоставление функции index с запросом к корню веб-приложения:

1
2
3
4
5
6
from django.urls import path
from hello import views
 
urlpatterns = [
    path("", views.index),
]
Связь шаблона template и view в Django
И запустим проект на выполнение и перейдем к приложению в браузере (если проект запущен, то его надо перезапустить):

Шаблоны в веб-приложении на Django и python
Подобным образом можно указать и другие шаблоны. Например, в папку templates добавим еще две страницы: about.html и contact.html

Шаблоны в Python и Django
И также в файле views.py определим функции, которые используют данные шаблоны:

1
2
3
4
5
6
7
8
9
10
from django.shortcuts import render
 
def index(request):
    return render(request, "index.html")
 
def about(request):
    return render(request, "about.html")
 
def contact(request):
    return render(request, "contact.html")
А в файле urls.py свяжем функции с маршрутами:

1
2
3
4
5
6
7
8
from django.urls import path
from hello import views
 
urlpatterns = [
    path("", views.index),
    path("about/", views.about),
    path("contact/", views.contact),
]
TemplateResponse
Выше для генерации шаблона применялась функция render(), которая является наиболее распространенным вариантом. Однако также мы можем использовать класс TemplateResponse:

1
2
3
4
from django.template.response import TemplateResponse
  
def index(request):
    return TemplateResponse(request,  "index.html")
    '''
    data = {"body":bodyHtml.html_content}    
    return render(request, "index.html", context=data)

def about(request):
    bodyHtml = TestTexts.objects.get(page_name="about")
    data = {"body":bodyHtml.html_content}
    return render(request, "about.html",context=data)
 
def contact(request):
    bodyHtml = TestTexts.objects.get(page_name="contact")
    contacts = Contacts.objects.all()
    data = {"body":bodyHtml.html_content, "contacts":contacts}
    return render(request, "contact.html",context=data)