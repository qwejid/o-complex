### Приложение для просмотра погоды на Django

Это веб-приложение разработано на Django для получения текущей погоды и прогноза на ближайшие 24 часа для выбранных пользователем городов. Приложение использует открытое API для получения данных о погоде и сохраняет историю запросов пользователей.

#### Установка

1. **Клонирование репозитория:**

   ```bash
   git clone <URL репозитория>
   cd o-complex
   ```

2. **Установка зависимостей:**

   Создайте виртуальное окружение и активируйте его, затем установите зависимости:

   ```bash
   python -m venv venv
   source venv\Scripts\activate 
   pip install -r requirements.txt
   ```

3. **Настройка базы данных:**

   Укажите настройки базы данных в файле `settings.py`:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'db.sqlite3',
       }
   }
   ```

   Можно также использовать другие базы данных, поддерживаемые Django.

4. **Применение миграций:**

   Примените миграции Django для создания таблиц в базе данных:

   ```bash
   python manage.py migrate
   ```

5. **Запуск сервера:**

   Запустите сервер разработки Django:

   ```bash
   python manage.py runserver
   ```

   Приложение будет доступно по адресу `http://127.0.0.1:8000/`.

#### Использование

1. **Форма ввода города:**

   На главной странице приложения пользователю предлагается ввести название города в форму и нажать кнопку "Получить прогноз".

2. **Отображение данных о погоде:**

   После отправки формы отображается текущая погода и прогноз на ближайшие 10 часов для выбранного города начиная с времени отправки.

3. **История запросов:**

   В приложении реализована функция сохранения истории запросов пользователей представлены последние 5 запросов. На странице также предсталяется обратится к последнему запросу пользователя.

#### Технологии

- **Django**: Фреймворк для разработки веб-приложений на Python.
- **OpenWeather API**: API для получения данных о погоде.
- **Geopy**: Библиотека для работы с геокодированием.
- **PostgreSQL**: База данных.

Этот проект создан в образовательных целях для изучения Django и интеграции с внешними API.
