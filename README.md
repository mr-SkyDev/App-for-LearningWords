# App for LearningWords
## Содержание
1. [Описание проекта](#description) 
2. [Используемые технологии](#technologies)
3. [Проектирование](#designing)
---
<a name="description"></a>  

## Описание
Десктопное *(позже, возможно, мобильное)* приложение для :book:изучения:book: новых слов как **русских**, так и **иностранных**

* Будет **неопределенное** количество курсов на выбор по изучению слов:
    * *русский*,
    * *английский*,
    * *собственный* (подробнее: [Свой курс](#ur-list))  
    (список будет расширяться).

    Можно будет выбрать **несколько** курсов.
* У курсов будет сложность:
    * базовый,
    * продвинутый,
    * профессиональный,
    * литературный  
    (Список, вероятно, будет расширяться).
* <a name='ur-list'></a> 
  Также можно будет создать свой курс слов, в котором будут слова, добавляемые пользователем.  
  Если человек желает добавить **собственное** слово, то будет проверяться правильность ввода. Пользователь может отключить проверку на это слово, но затем он **должен** будет дать ему определение. Иначе определение не будет найдено.
* Словам можно будет давать определение **вручную**. Иначе определение будет браться из интернета (будет использоваться определённый источник).
* Приложение для корректной работы должно быть в **автозагрузке** и работать в **фоновом режиме**.
* Слово и его значение будет отображаться в уведомлении. В том же уведомлении будут кнопки **«понял»** **«выучил»**. Первая закрывает уведомление, а вторая так же закрывает, но и удаляет это слово из **БД** слов для изучения.
* Будет поле для поиска определения слова, введённого пользователем

---
<a name="technologies"></a>

## Какие технологии будут использоваться
* PyQt5 — для создания тела приложения
* SQLite — для создания базы данных слов
* :link:[win10toast](https://github.com/jithurjacob/Windows-10-Toast-Notifications) / :link:[NotificationHub](https://docs.microsoft.com/ru-ru/azure/notification-hubs/notification-hubs-python-push-notification-tutorial) / :link:[Plyer](https://docs.microsoft.com/ru-ru/azure/notification-hubs/notification-hubs-python-push-notification-tutorial) — для настройки уведомлений 
* BeautifulSoup4 — для парсинга сайтов

---
<a name="designing"></a>

## Этапы разработки
### 1. Составить базу данных слов (для начала: английский и русский)  
  > Так как я не нашел уже готовую базу данных слов, я буду парсить сайт https://slovaronline.com/. И из полученных данных будет создаваться
### 2. Создать интерфейс приложения
### 3. Добавить бэкэнд
### 4. Связать БД с программой
### 5. Настроить уведомления
  > Есть 2 варианта:
  > * Использовать уведомления Windows 
  > * Использовать **свои** всплывающие окна
### 6. Скомпилировать в <i>.exe</i>
