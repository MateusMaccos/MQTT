import tkinter as tk
import paho.mqtt.client as mqtt


class Sensor:
    def __init__(self, nome, parametro, minimo, maximo):
        self.nome = nome
        self.parametro = parametro
        self.minimo = minimo
        self.maximo = maximo
        self.valor_atual = 0
        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION1,
        )
        self.client.connect(host="test.mosquitto.org", port=1883)
        self.client.loop_start()

    def ler_valor_atual(self):
        self.client.publish(
            topic=f"sensor/{self.nome}",
            payload=f"Valor lido: {self.valor_atual}",
        )

    def set_valor_atual(self, valor):
        self.valor_atual = valor
        if valor == self.minimo:
            self.client.publish(f"sensor/{self.nome}", f"Atingiu valor mínimo: {valor}")
        elif valor == self.maximo:
            self.client.publish(f"sensor/{self.nome}", f"Atingiu valor máximo: {valor}")
        if valor < self.minimo or valor > self.maximo:
            self.client.publish(f"sensor/{self.nome}", f"Valor fora do limite: {valor}")


class Cliente:
    def __init__(self):
        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION1,
        )
        self.client.on_message = self.on_message
        self.client.connect(host="test.mosquitto.org", port=1883)
        self.client.loop_start()
        self.client.subscribe("sensor/+/+")
        self.client.message_callback_add("sensor/+/+", self.processar_mensagem)
        self.opcoes_disponiveis = []
        self.opcoes_selecionadas = []

    def desenhar_painel(self, tela, opcoes_disponiveis):
        self.lb_opcoes_disponiveis = tk.Listbox(tela, selectmode=tk.MULTIPLE)
        self.lb_opcoes_disponiveis.pack(padx=10, pady=10)

        for opcao in opcoes_disponiveis:
            self.lb_opcoes_disponiveis.insert(tk.END, opcao.nome)
            self.opcoes_disponiveis.append(opcao.nome)

        self.lb_opcoes_escolhidas = tk.Listbox(tela, selectmode=tk.SINGLE)
        self.lb_opcoes_escolhidas.pack(padx=10, pady=10)

        self.btn_assinar = tk.Button(tela, text="Assinar", command=self.assinar)
        self.btn_assinar.pack(pady=5)

        self.btn_assinar = tk.Button(
            tela, text="Remover assinatura", command=self.removerAssinatura
        )
        self.btn_assinar.pack(pady=10)

    def processar_mensagem(self, client, userdata, message):
        topico = message.topic
        sensor, parametro = topico.split("/")[1:]
        valor = message.payload.decode()
        self.lbl_mensagens_recebidas.config(
            text=f"Mensagem recebida do sensor {sensor}: {parametro}: {valor}"
        )

    def on_message(self, client, userdata, message):
        pass

    def assinar(self):
        selecao = self.lb_opcoes_disponiveis.curselection()
        for index in selecao:
            opcao = self.opcoes_disponiveis[index]
            if opcao not in self.opcoes_selecionadas:
                self.opcoes_selecionadas.append(opcao)
                self.lb_opcoes_escolhidas.insert(tk.END, opcao)

    def removerAssinatura(self):
        selecao = self.lb_opcoes_escolhidas.curselection()[0]
        opcao = self.opcoes_selecionadas[selecao]
        self.opcoes_selecionadas.remove(opcao)
        self.lb_opcoes_escolhidas.delete(selecao)


class Aplicacao:
    def __init__(self):
        self.sensores = [
            Sensor("Sensor1", "temperatura", 20, 30),
            Sensor("Sensor2", "umidade", 40, 60),
            Sensor("Sensor3", "velocidade", 0, 100),
        ]
        self.clientes = [
            Cliente(),
        ]
        self.tela = None

    def adicionarSensor(self, nome, parametro, min, max):
        self.sensores.append(Sensor(nome, parametro, min, max))

    def adicionarCliente(self):
        self.clientes.append(Cliente())

    def run(self):
        self.tela = tk.Tk()
        self.tela.title("Comunicação MQTT")
        self.tela.geometry("500x500")

        for cliente in self.clientes:
            cliente.desenhar_painel(self.tela, self.sensores)

        self.lbl_mensagens = tk.Label(self.tela, text="Mensagens:")
        self.lbl_mensagens.pack(pady=5)

        self.lbl_mensagens_recebidas = tk.Label(self.tela, text="")
        self.lbl_mensagens_recebidas.pack()
        self.tela.mainloop()


if __name__ == "__main__":
    global app
    app = Aplicacao()
    app.run()
