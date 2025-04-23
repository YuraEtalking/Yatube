# api_final_yatube

## Описание.
Yatube - это современная социальная платформа для ведения блогов, которая 
предоставляет полноценный функционал для создания и управления контентом.

Основные возможности платформы:

- Регистрация личного аккаунта
- Публикация авторских постов
- Редактирование и удаление собственных публикаций
- Взаимодействие с другими авторами через комментарии
- Система подписок на интересных блогеров
- API-интерфейс для программного взаимодействия с платформой

> У неаутентифицированных пользователей доступ к API разрешен только для чтения.
> Исключение эндпоинты подписок.  
> **Подписки:**   
> <span style="color: #58b216;">GET</span>
> `http://127.0.0.1:8000/api/v1/follow/`
> 
> **Информация о сообществе:**   
> <span style="color: #6091ff;">POST</span>
> `http://127.0.0.1:8000/api/v1/follow/`

## Установка.

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/YuraEtalking/api_final_yatube.git
```

```
cd yatube_api 
```

Cоздать и активировать виртуальное окружение:


```
python -m venv env
```

```
.\venv\Scripts\activate
```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```
## Некоторые примеры запросов к API.

### Получение JWT токена (аутентификация):
<br>

>Токен действителен 1 день, для изменения нужно изменить настройки `SIMPLE_JWT` 
ключ `ACCESS_TOKEN_LIFETIME` в `settings.py`

<span style="color: #6091ff;">POST</span> 
`http://127.0.0.1:8000/api/v1/jwt/create/`

<br>

**Request**
```
{
  "username": "string",
  "password": "string"
}
```
<br>

**Response  <span style="color: #7ee434;">200</span>**
```
{
  "refresh": "string",
  "access": "string"
}
```
<br>

**Response  <span style="color: #ee2f4e;">400</span>**
```
{
  "username": [
    "Обязательное поле."
  ],
  "password": [
    "Обязательное поле."
  ]
}
```
<br>

**Response  <span style="color: #ee2f4e;">401</span>**
```
{
  "detail": "Не найдено активной учетной записи с указанными учетными данными"
}
```
<br>

### Получение публикации:


<span style="color: #58b216;">GET</span> 
`http://127.0.0.1:8000/api/v1/posts/{id}/`

<br>

**Response  <span style="color: #7ee434;">200</span>**
```
{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2019-08-24T14:15:22Z",
  "image": "string",
  "group": 0
}
```
<br>

**Response  <span style="color: #ee2f4e;">404</span>**
```
{
  "detail": "Страница не найдена."
}
```
<br>

### Получение списка публикаций:

> При указании параметров limit и offset выдача будет работать с пагинацией.
`http://127.0.0.1:8000/api/v1/posts/?offset=2&limit=2`

<br>

<span style="color: #58b216;">GET</span>
`http://127.0.0.1:8000/api/v1/posts/`



**Response  <span style="color: #7ee434;">200</span>**
```
{
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=400&limit=100",
  "previous": "http://api.example.org/accounts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "author": "string",
      "text": "string",
      "pub_date": "2021-10-14T20:41:29.648Z",
      "image": "string",
      "group": 0
    }
  ]
}
```
<br>
<br>

### Эндпоинты:
<br>

**Создание публикации:**   
<span style="color: #6091ff;">POST</span>
`http://127.0.0.1:8000/api/v1/posts/`


**Обновление публикации:**   
<span style="color: #bc52ff;">PUT</span>
`http://127.0.0.1:8000/api/v1/posts/{id}/`

**Частичное обновление публикации:**   
<span style="color: #ffac52;">PATCH</span>
`http://127.0.0.1:8000/api/v1/posts/{id}/`

**Удаление публикации:**   
<span style="color: #ee2f4e;">DELETE</span>
`http://127.0.0.1:8000/api/v1/posts/{id}/`

<br>

**Получение списка комментариев:**   
<span style="color: #58b216;">GET</span>
`http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/`

**Добавление комментария:**   
<span style="color: #6091ff;">POST</span>
`http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/`

**Получение комментария:**   
<span style="color: #58b216;">GET</span>
`http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/{id}/`

**Обновление комментария:**   
<span style="color: #bc52ff;">PUT</span>
`http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/{id}/`

**Частичное обновление комментария:**   
<span style="color: #ffac52;">PATCH</span>
`http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/{id}/`

**Удаление комментария:**   
<span style="color: #ee2f4e;">DELETE</span>
`http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/{id}/`

<br>

**Список сообществ:**   
<span style="color: #58b216;">GET</span>
`http://127.0.0.1:8000/api/v1/groups/`

**Информация о сообществе:**   
<span style="color: #58b216;">GET</span>
`http://127.0.0.1:8000/api/v1/groups/{id}/`

<br>

**Подписки:**   
<span style="color: #58b216;">GET</span>
`http://127.0.0.1:8000/api/v1/follow/`

**Информация о сообществе:**   
<span style="color: #6091ff;">POST</span>
`http://127.0.0.1:8000/api/v1/follow/`

<br>

**Обновить JWT-токен:**   
<span style="color: #6091ff;">POST</span>
`http://127.0.0.1:8000/api/v1/jwt/refresh/`

**Проверить JWT-токен:**   
<span style="color: #6091ff;">POST</span>
`http://127.0.0.1:8000/api/v1/jwt/verify/`
