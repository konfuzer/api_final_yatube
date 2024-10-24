
## Описание
Проект представляет собой API для социальной сети Yatube, где пользователи могут публиковать посты, комментировать записи и подписываться друг на друга. API позволяет работать с основными функциями сайта через HTTP-запросы.

## Установка
1. Клонируйте репозиторий:
   ```
   git clone https://github.com/ваш-репозиторий/api_final_yatube.git
   ```
2. Перейдите в директорию проекта:
   ```
   cd api_final_yatube
   ```
3. Создайте и активируйте виртуальное окружение:
   ```
   python -m venv venv
   source venv/bin/activate  # для Windows: venv\Scripts\activate
   ```
4. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```
5. Выполните миграции:
   ```
   python manage.py migrate
   ```
6. Запустите проект:
   ```
   python manage.py runserver
   ```

## Примеры запросов к API

### Получение списка постов:
```
GET /api/posts/
```

### Создание нового поста (требуется аутентификация):
```
POST /api/posts/
Content-Type: application/json
{
  "text": "Новый пост",
  "group": 1
}
```

### Получение комментариев к посту:
```
GET /api/posts/{post_id}/comments/
```

### Подписка на пользователя (требуется аутентификация):
```
POST /api/follow/
Content-Type: application/json
{
  "following": "username"
}
```
