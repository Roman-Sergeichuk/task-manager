# task-manager

## Описание
Персонализированный сервис, позволяющий пользователю ставить себе задачи, отражать в системе изменение их статуса и просматривать историю задач.

## Функциональные возможности

- взаимодействие с приложением осуществляется посредством JSON API;
- реализована авторизация пользователей; 
- в системе может быть зарегистрировано множество пользователей;
- пользователь после авторизации может создавать себе задачу, указав  для этого ее название, описание,  планируемое время завершения и статус;
- пользователь может редактировать содержимое любой своей задачи;
- пользователь может удалить любую из ранее созданных своих задач;
- пользователь может вывести список своих задач с возможностью фильтрации по статусу и планируемой дате завершения;
- пользователь может прсматривать историю изменения любой своей задачи.

## Запуск приложения

Для запуска приложения, склонируйте репозиторий:

    git clone https://github.com/Roman-Sergeichuk/task-manager.git

Активируйте виртуальное окружение и установите необходимые зависимости, выполнив команду:

    pip install -r requirements.txt
    
Приложение настроено на работу с базой данных PostgreSQL, поэтому необходимо зайти в settings.py и установить значения для своей базы данных в переменной «DATABASES».
После этого нужно сделать и применить миграции:

    python manage.py makemigrations
    python manage.py migrate
    
Теперь запустите сервер, выполнив команду:

    python manage.py runserver
    
Для запуска тестов используйте команду:

    python manage.py test
    
## Пример использования приложения

Регистрируем нового пользователя:

    curl -X POST http://127.0.0.1:8000/auth/users/ -H 'Content-Type: application/json' --data '{"username": "postman5", "password": "alpine12"}'
    
    {"email":"","username":"postman5","id":7}

В ответе мы получили данные нашего нового пользователя в виде JSON. Это говорит о том, что пользователь успешно зарегистрировался в системе.

Авторизуемся в системе, введя имя пользователя и пароль:

    curl -X POST http://127.0.0.1:8000/auth/token/login/ -H 'Content-Type: application/json' --data '{"username": "postman5", "password": "alpine12"}'
    
    {"auth_token":"b5ef40322180df95034ce9b41af2adae702bca39"}
    
В ответе мы получили токен, который нам понадобится для совершения дальнейших действий в системе от лица нашего пользователя.

### Создание задач
При создании задачи в теле запроса нужно заполнить следующие поля: 
- "title" - название задачи;
- "description" — описание задачи;
- "completion_date" — планируемая дата завершения;
- "status" — статус задачи (один из: "NEW", "PLANNED", "IN_PROGRESS", "COMPLETED". По умолчанию устанавливается "NEW").

Создадим новую задачу, не забывая указать наш раннее полученный токен в заголовке "Authorization":

    curl -X POST http://127.0.0.1:8000/tasks/ -H 'Content-Type: application/json' -H 'Authorization: Token b5ef40322180df95034ce9b41af2adae702bca39'  --data '{"title": "Go to the shop", "description": "Buy milk and bread", "completion_date": "2020-10-10"}'
    
    {"id":14,"author":"postman5","created_date":"2020-10-05T12:36:56.673953+03:00","title":"Go to the shop","description":"Buy milk and bread","completion_date":"2020-10-10","status":"NEW"}

В ответе мы получили JSON с данными нашей задачи.
Создадим еще одну задачу со статусом "PLANNED":

    curl -X POST http://127.0.0.1:8000/tasks/ -H 'Content-Type: application/json' -H 'Authorization: Token b5ef40322180df95034ce9b41af2adae702bca39'  --data '{"title": "Clean at home", "description": "Wash the floor", "completion_date": "2020-10-05"}'
    
    {"id":15,"author":"postman5","created_date":"2020-10-05T12:59:29.613606+03:00","title":"Clean at home","description":"Wash the floor","completion_date":"2020-10-05","status":"PLANNED"}
    
Выведем список ранее созданных задач:

    curl -X GET http://127.0.0.1:8000/tasks/ -H 'Content-Type: application/json' -H 'Authorization: Token b5ef40322180df95034ce9b41af2adae702bca39'
    
    {"count":2,"next":null,"previous":null,"results":[{"id":15,"author":"postman5","created_date":"2020-10-05T12:59:29.613606+03:00","title":"Clean at home","description":"Wash the floor","completion_date":"2020-10-05","status":"PLANNED"},{"id":14,"author":"postman5","created_date":"2020-10-05T12:36:56.673953+03:00","title":"Go to the shop","description":"Buy milk and bread","completion_date":"2020-10-10","status":"NEW"}]}

Отфильтруем наши задачи по статусу:

    curl X GET http://127.0.0.1:8000/tasks/?status=NEW -H 'Content-Type: application/json' -H 'Authorization: Token b5ef40322180df95034ce9b41af2adae702bca39'
    
    {"count":1,"next":null,"previous":null,"results":[{"id":14,"author":"postman5","created_date":"2020-10-05T12:36:56.673953+03:00","title":"Go to the shop","description":"Buy milk and bread","completion_date":"2020-10-10","status":"NEW"}]}
    
Отфильтруем наши задачи по дате завершения:

    curl X GET http://127.0.0.1:8000/tasks/?planned_date=2020-10-05 -H 'Content-Type: application/json' -H 'Authorization: Token b5ef40322180df95034ce9b41af2adae702bca39'
    
    {"count":1,"next":null,"previous":null,"results":[{"id":15,"author":"postman5","created_date":"2020-10-05T12:59:29.613606+03:00","title":"Clean at home","description":"Wash the floor","completion_date":"2020-10-05","status":"PLANNED"}]}
    
### Редактирование задач

Изменим статус в нашей задаче с id=15:

    curl -X PUT http://127.0.0.1:8000/tasks/15/ -H 'Content-Type: application/json' -H 'Authorization: Token b5ef40322180df95034ce9b41af2adae702bca39'  --data '{"title": "Clean at home", "description": "Wash the floor", "completion_date": "2020-10-05", "status": "IN_PROGRESS"}'
    
    {"id":15,"author":"postman5","created_date":"2020-10-05T12:59:29.613606+03:00","title":"Clean at home","description":"Wash the floor","completion_date":"2020-10-05","status":"IN_PROGRESS"}
    
Теперь удалим эту задачу:

    curl -X DELETE http://127.0.0.1:8000/tasks/15/ -H 'Content-Type: application/json' -H 'Authorization: Token b5ef40322180df95034ce9b41af2adae702bca39'
    
### Просмотр истории изменения задач

Выведем историю изменения задачи с id=15:

    curl -X GET http://127.0.0.1:8000/history/?task_id=15 -H 'Content-Type: application/json' -H 'Authorization: Token b5ef40322180df95034ce9b41af2adae702bca39'
    
    {"count":2,"next":null,"previous":null,"results":[{"id":14,"task_id":15,"title":"Clean at home","description":"Wash the floor","created_date":"2020-10-05T13:24:04.685248+03:00","completion_date":"2020-10-05","status":"IN_PROGRESS","author":7},{"id":13,"task_id":15,"title":"Clean at home","description":"Wash the floor","created_date":"2020-10-05T12:59:29.637971+03:00","completion_date":"2020-10-05","status":"PLANNED","author":7}]}