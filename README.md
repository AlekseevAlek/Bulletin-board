# Bulletin-board
Данный проект реализует доску объявлений с помощью фреймворка Django.
Програма позволяет создавать новых пользователей, добавлять новые объявления и просматривать существующие.

Задача №1. Реализовать функционал: Правка объявлений.

Создаём новое представление (view) с помощью функции edit_advertisement для редактирования объявлений, которое загружает форму существующего объявления и сохраняет изменения.

Добавляем URL для нового представления в urls.py.

Создаём шаблон edit_advertisement.html для формы редактирования, аналогичный шаблону добавления объявления, но с загруженными данными.

Задача №2. Реализовать функционал: Удаление объявлений.

Создаём представление с помощью функции delete_advertisement для удаления объявлений, которое удаляет выбранное объявление после подтверждения пользователя.

Добавляем URL для этого представления в urls.py.

Создаём шаблон delete_advertisement.html с формой подтверждения удаления объявления.

Задача №3. Реализовать функционал: Добавление изображений к объявлениям.

- Добавляем ImageField в модель объявления в models.py.
  
- Устанфвливаем Pillow для обработки изображений (pip install Pillow).
  
- Обновляем форму объявления в forms.py, добавив поле для изображения.
  
- Изменяем шаблоны для отображения изображений в объявлениях.

Задача №4. Добавление имени автора к объявлению.

Добавляем в шаблоны отображение advertisement.author.username там, где необходимо показать автора объявления.

Задача №5. Добавление лаайков и дизлайков.

- Расширяем модель объявления в models.py, добавив поля для подсчёта лайков и дизлайков.

- Создаём представления для обработки действий лайка/дизлайка.

- Добавляем URL и обновяем шаблоны для отображения и обработки лайков и дизлайков.

Задача №6. Сохранение количества созданных объявлений.

-Создаём модель профиля пользователя, чтобы хранить статистику.

-Используем сигналы Django или переопределить методы, чтобы обновлять статистику при создании/удалении объявлений и при лайках/дизлайках (если уже добавлены лайки и дизлайки).

Задача №7. Добавление пагинации (ограничения количества объявлений на странице).

-Изменяем представление списка объявлений, чтобы использовать Paginator из django.core.paginator.

-Обновляем шаблон списка объявлений, добавив элементы управления пагинацией.


