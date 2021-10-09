# App for LearningWords
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

---
## Какие технологии будут использоваться
* PyQt5 — для создания тела приложения
* SQLite — для создания базы данных слов
* win10toast / NotificationHub / Plyer — для настройки уведомлений 