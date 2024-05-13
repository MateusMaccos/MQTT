from application.configs.broker_configs import mqtt_broker_configs


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Cliente conectado com sucesso: {client}")
        client.subscribe(mqtt_broker_configs["TOPIC"])
    else:
        print(f"Deu erro ao conectar: {rc}")


def on_subscribe(client, userdata, mid, granted_qos):
    print(f'Cliente inscreveu no topico: {mqtt_broker_configs["TOPIC"]}')
    print(f"qos: {granted_qos}")


def on_message(client, userdata, message):
    print("Mensagem recebida")
    print(client)
    print(message.payload)
