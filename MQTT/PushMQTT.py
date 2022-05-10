import time
import paho.mqtt.client as mqtt

MQTTHOST = "srv2.clusterfly.ru"  # IP-адрес сервера MQTT
MQTTPORT = 9994  # MQTT номер порта сервера
ClientId = "clientId-UobqV7tpQi" + str(time.time())  # ClientId должен быть уникальным
username = "user_33f73928"  # имя пользователя
password = "pass_74a9e7f0"  # Имя пользователя соответствующий пароль
message_received: str


def get_temperature_in_valve(self):
    mqtt_client = mqtt.Client(ClientId)
    mqtt_client.username_pw_set(username, password)  # Установите имя пользователя и доступный пароль
    mqtt_client.on_connect = self.mqtt_get_connected  # Установите функцию обратного вызова для успешного подключения
    mqtt_client.on_message = self.on_message  # Установить функцию обратного вызова для получения данных темы подписки
    mqtt_client.on_subscribe = self.on_subscribe  # Установить функцию обратного вызова для успешной подписки на тему
    mqtt_client.on_disconnect = self.on_disconnect  # Установить функцию обратного вызова при потере соединения

    # Клиент подключается к прокси-серверу, время биения 60
    mqtt_client.connect(MQTTHOST, MQTTPORT, 60)
    # Блокирующая форма сетевого цикла не вернется, пока клиент не вызовет disconnect (). Он автоматически обработает переподключение
    return mqtt_client.on_message()


def mqtt_get_connected(mqttClient, rc):
    if not rc:
        print("MQTT connect success.")
        mqttClient.publish("PidValue", "I'm python", qos=0)  # отправить сообщения
        mqttClient.subscribe("temperature_in_valve", qos=0)  # Подпишитесь на темы
    else:
        print("MQTT connect error:", rc)


# Функция обратного вызова успешного соединения Параметры: экземпляр клиента, который вызывает функцию обратного
# вызова, личные данные пользователя, словарь, содержащий знак ответа прокси, и статус соединения
def mqtt_connected(mqttClient, userdata, flags, rc):
    if not rc:
        print("MQTT connect success.")
        mqttClient.publish("temperature_in_valve", "I'm python", qos=0)  # отправить сообщения
        mqttClient.subscribe("Python_subscribe", qos=0)  # Подпишитесь на темы
    else:
        print("MQTT connect error:", rc)

    # Получение функции обратного вызова данных о подписке


def on_message(client, userdata, msg):
    print("тема:", msg.topic, "Сообщение:")
    print(str(msg.payload.decode('utf-8')))
    return str(msg.payload.decode("utf-8"))

    # Функция обратного вызова успешной темы подписки


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscrib topic success,qos = %d" % granted_qos)

    # Функция обратного вызова при потере соединения


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection %s" % rc)


def push_mail(PidValue):
    # Создаем коммуникационный объект mqtt
    mqtt_client = mqtt.Client(ClientId)
    mqtt_client.username_pw_set(username, password)
    mqtt_client.connect(MQTTHOST, MQTTPORT, 60)
    mqtt_client.loop_start()
    mqtt_client.publish("Server/PidValue", PidValue)
    # Блокирующая форма сетевого цикла не вернется, пока клиент не вызовет disconnect (). Он автоматически обработает переподключение
    mqtt_client.loop_stop()
    mqtt_client.on_disconnect = on_disconnect
