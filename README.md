# notification_bot

Телеграм-бот присылает результат проверки работы на курсе [dvmn.org](https://dvmn.org/)

### Как установить

Создайте .env файл с содержимым
```
DEVMAN_TOKEN=''
TG_TOKEN=''
TG_CHAT_ID=''
```
На [странице про API Девмана]https://dvmn.org/api/docs/ найдите персональный токен и вставьт его в первую строку .env файла. <br/>

Напишите в телеграм боту @userinfobot, чтобы узнать свой id. Вставьте его в третью строчку .env файла. <br/> <br/>

Установите зависимости:
```
pip install -r requirements.txt
```
(Python3 должен быть уже установлен)

### Пример запуска

```
main.py
```

### Пример оповещения от бота
![image](https://user-images.githubusercontent.com/52741545/124275072-b2471d80-db4a-11eb-9905-dc06dbf0317a.png)

