from application.configs.broker_configs import mqtt_broker_configs


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Cliente conectado com sucesso: {client}")
        for topico in mqtt_broker_configs["TOPICS"]:
            print(f"Cliente se inscreveu no tópico: {topico}")
            client.subscribe(topico)
        client.unsubscribe(mqtt_broker_configs["TOPICS"][0])
    else:
        print(f"Deu erro ao conectar: {rc}")


def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Cliente inscreveu corretamente!")


def on_unsubscribe(client, userdata, mid):
    print(f"Cliente desinscreveu corretamente!")


def on_message(client, userdata, message):
    print("Mensagem recebida")
    print(client)
    print(message.payload)
