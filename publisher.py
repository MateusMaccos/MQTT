import paho.mqtt.client as mqtt

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "meu_publisher")
mqtt_client.connect(host="test.mosquitto.org", port=1883)
mqtt_client.publish(topic="ppd2024MQTT", payload="valor:10")

print("Acabou")
