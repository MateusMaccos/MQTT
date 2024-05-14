import tkinter as tk
import paho.mqtt.client as mqtt


class Sensor:
    def __init__(self, nome):
        self.nome = nome
        self.parametro = None
        self.minimo = None
        self.maximo = None
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

    def ler_parametro(self):
        return self.parametro_selecionado.get()

    def ler_max(self):
        return self.parametro_selecionado.get()

    def ler_min(self):
        return self.parametro_selecionado.get()

    def set_valor_atual(self):
        self.valor_atual = self.campo_valor_atual.get()
        if self.valor_atual not in [None, ""]:
            print(self.valor_atual)
        else:
            print("Digitou nada")
        # if self.valor_atual == self.minimo:
        #     self.client.publish(
        #         f"sensor/{self.nome}", f"Atingiu valor mínimo: {self.valor_atual}"
        #     )
        # elif self.valor_atual == self.maximo:
        #     self.client.publish(
        #         f"sensor/{self.nome}", f"Atingiu valor máximo: {self.valor_atual}"
        #     )
        # if self.valor_atual < self.minimo or self.valor_atual > self.maximo:
        #     self.client.publish(
        #         f"sensor/{self.nome}", f"Valor fora do limite: {self.valor_atual}"
        #     )

    def set_valor_min(self):
        pass

    def set_valor_max(self):
        pass

    def set_parametro(self):
        pass

    def desenhar_painel(self, tela):
        tela_sensor = tk.Frame(tela)
        tela_sensor.pack(pady=5)

        frame_config = tk.Frame(tela_sensor)
        frame_config.pack(pady=5)

        self.lbl_cliente = tk.Label(frame_config, text=f"Sensor {self.nome}")
        self.lbl_cliente.pack(padx=20, side=tk.LEFT)

        self.frame_param_valor = tk.Frame(frame_config)
        self.frame_param_valor.pack(padx=10, side=tk.LEFT)

        # Lista de opções
        opcoes = ["Temperatura", "Umidade", "Velocidade"]

        # Variável para armazenar a opção selecionada
        self.parametro_selecionado = tk.StringVar(self.frame_param_valor)
        self.parametro_selecionado.set(opcoes[0])  # Define o valor padrão

        # Criação do dropdown
        self.dropdown = tk.OptionMenu(
            self.frame_param_valor, self.parametro_selecionado, *opcoes
        )
        self.dropdown.pack(pady=20)

        self.lbl_cliente = tk.Label(self.frame_param_valor, text="Valor Atual: ")
        self.lbl_cliente.pack(padx=20)

        self.campo_valor_atual = tk.Entry(self.frame_param_valor)
        self.campo_valor_atual.pack(pady=20)

        self.frame_min_max = tk.Frame(frame_config)
        self.frame_min_max.pack(padx=20, side=tk.RIGHT)

        self.lbl_cliente = tk.Label(self.frame_min_max, text="Valor Mínimo: ")
        self.lbl_cliente.pack(padx=20)

        self.campo_valor_min = tk.Entry(self.frame_min_max)
        self.campo_valor_min.pack(pady=20)

        self.lbl_cliente = tk.Label(self.frame_min_max, text="Valor Máximo: ")
        self.lbl_cliente.pack(padx=20)

        self.campo_valor_max = tk.Entry(self.frame_min_max)
        self.campo_valor_max.pack(pady=20)

        separator = tk.Frame(tela_sensor, height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill="x", padx=5, pady=5, side=tk.BOTTOM)


class Cliente:
    def __init__(self, id):
        self.id = id
        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION1,
        )
        self.client.on_message = self.on_message
        self.client.connect(host="test.mosquitto.org", port=1883)
        self.client.loop_start()
        # self.client.subscribe("sensor/+/+")
        # self.client.message_callback_add("sensor/+/+", self.processar_mensagem)
        self.opcoes_disponiveis = []
        self.opcoes_selecionadas = []
        self.mensagens = []

    def desenhar_painel(self, tela, opcoes_disponiveis):
        tela_cliente = tk.Frame(tela)
        tela_cliente.pack(pady=5)

        frame_config = tk.Frame(tela_cliente)
        frame_config.pack(pady=5)

        self.lbl_cliente = tk.Label(frame_config, text=f"Cliente {self.id}")
        self.lbl_cliente.pack(padx=20, side=tk.LEFT)

        frame_sensores = tk.Frame(frame_config)
        frame_sensores.pack(pady=5, side=tk.LEFT)

        self.lbl_sensores_disp = tk.Label(frame_sensores, text="Sensores:")
        self.lbl_sensores_disp.pack(side=tk.TOP)
        self.lb_opcoes_disponiveis = tk.Listbox(frame_sensores, selectmode=tk.MULTIPLE)
        self.lb_opcoes_disponiveis.pack(padx=10, pady=10)

        frame_mensagens = tk.Frame(frame_config)
        frame_mensagens.pack(pady=5, side=tk.RIGHT)

        self.lbl_mensagens = tk.Label(frame_mensagens, text="Medições:")
        self.lbl_mensagens.pack(side=tk.TOP)
        self.lb_mensagens = tk.Listbox(frame_mensagens, width=50, height=10)
        self.lb_mensagens.pack(pady=10)

        for opcao in opcoes_disponiveis:
            self.lb_opcoes_disponiveis.insert(tk.END, opcao.nome)
            self.opcoes_disponiveis.append(opcao.nome)

        frame_sensores_inscritos = tk.Frame(frame_config)
        frame_sensores_inscritos.pack(pady=5, side=tk.RIGHT)

        self.lbl_sensores_assinados = tk.Label(
            frame_sensores_inscritos, text="Sensores inscritos:"
        )
        self.lbl_sensores_assinados.pack(side=tk.TOP)
        self.lb_opcoes_escolhidas = tk.Listbox(
            frame_sensores_inscritos, selectmode=tk.SINGLE
        )
        self.lb_opcoes_escolhidas.pack(padx=10, pady=10)

        frame_btn = tk.Frame(frame_config)
        frame_btn.pack(pady=5)

        self.btn_assinar = tk.Button(frame_btn, text="Assinar", command=self.assinar)
        self.btn_assinar.pack(pady=(50, 0))

        self.btn_tirar_assinatura = tk.Button(
            frame_btn, text="Remover assinatura", command=self.removerAssinatura
        )
        self.btn_tirar_assinatura.pack(pady=5)

        separator = tk.Frame(tela_cliente, height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill="x", padx=5, pady=5, side=tk.BOTTOM)

    def processar_mensagem(self, client, userdata, message):
        topico = message.topic
        sensor, parametro = topico.split("/")[1:]
        valor = message.payload.decode()
        self.lbl_mensagens_recebidas.config(
            text=f"Mensagem recebida do sensor {sensor}: {parametro}: {valor}"
        )

    def on_message(self, client, userdata, message):
        print(f"Mensagem recebida {message.topic}: {message.payload.decode()}")
        self.mensagens.append(f"{message.topic} mediu: {message.payload.decode()}")
        self.lb_mensagens.insert(
            tk.END, f"{message.topic} mediu: {message.payload.decode()}"
        )

    def assinar(self):
        selecao = self.lb_opcoes_disponiveis.curselection()
        for index in selecao:
            opcao = self.opcoes_disponiveis[index]
            if opcao not in self.opcoes_selecionadas:
                self.client.subscribe(str(opcao))
                self.opcoes_selecionadas.append(opcao)
                self.lb_opcoes_escolhidas.insert(tk.END, opcao)

    def removerAssinatura(self):
        try:
            selecao = self.lb_opcoes_escolhidas.curselection()[0]
            opcao = self.opcoes_selecionadas[selecao]
            self.opcoes_selecionadas.remove(opcao)
            self.lb_opcoes_escolhidas.delete(selecao)
            self.client.unsubscribe(str(opcao))
        except:
            print("Nenhuma opção selecionada")

    def atualiza_lista_sensores(self, novoSensor):
        self.opcoes_disponiveis.append(novoSensor.nome)
        self.lb_opcoes_disponiveis.insert(tk.END, novoSensor.nome)


class Aplicacao:
    def __init__(self):
        self.sensores = [
            Sensor(1),
            Sensor(2),
            Sensor(3),
        ]
        self.clientes = []
        self.tela = None
        self.telaSensores = None

    def adicionarSensor(self):
        sensor = Sensor(len(self.sensores) + 1)
        self.sensores.append(sensor)
        sensor.desenhar_painel(self.frame_sensores)
        # Atualiza as opções disponíveis em todos os clientes
        for cliente in self.clientes:
            cliente.atualiza_lista_sensores(sensor)

    def atualizarSensores(self):
        for sensor in self.sensores:
            sensor.set_valor_atual()
            sensor.set_valor_min()
            sensor.set_valor_max()
            sensor.set_parametro()

    def adicionarCliente(self):
        cliente = Cliente(len(self.clientes) + 1)
        self.clientes.append(cliente)
        cliente.desenhar_painel(self.frame_conteudo, self.sensores)

    def abrirTelaSensores(self):
        self.telaSensores = tk.Tk()
        self.telaSensores.title("Sensores MQTT")
        self.telaSensores.geometry("1000x500")

        # Cria um Canvas
        self.canvas2 = tk.Canvas(self.telaSensores)
        self.canvas2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Adiciona barras de rolagem
        self.scrollbar_vertical2 = tk.Scrollbar(
            self.telaSensores, orient=tk.VERTICAL, command=self.canvas2.yview
        )
        self.scrollbar_vertical2.pack(side=tk.RIGHT, fill=tk.Y)

        # Configuração do Canvas
        self.canvas2.configure(
            yscrollcommand=self.scrollbar_vertical2.set,
        )
        self.canvas2.bind("<Configure>", self.on_canvas_configure_sensor)

        # Adiciona um frame para o conteúdo
        self.frame_sensores = tk.Frame(self.canvas2)
        self.canvas2.create_window((0, 0), window=self.frame_sensores, anchor="nw")

        for sensor in self.sensores:
            sensor.desenhar_painel(self.frame_sensores)

        self.btn_add_sensor = tk.Button(
            self.telaSensores, text="Adicionar Sensores", command=self.adicionarSensor
        )
        self.btn_add_sensor.pack(pady=5, side=tk.TOP)

        self.btn_assinar = tk.Button(
            self.telaSensores, text="Atualizar dados", command=self.atualizarSensores
        )
        self.btn_assinar.pack()

        self.telaSensores.mainloop()

    def run(self):
        self.tela = tk.Tk()
        self.tela.title("Clientes MQTT")
        self.tela.geometry("1000x500")

        # Cria um Canvas
        self.canvas = tk.Canvas(self.tela)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Adiciona barras de rolagem
        self.scrollbar_vertical = tk.Scrollbar(
            self.tela, orient=tk.VERTICAL, command=self.canvas.yview
        )
        self.scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)

        # Configuração do Canvas
        self.canvas.configure(
            yscrollcommand=self.scrollbar_vertical.set,
        )
        self.canvas.bind("<Configure>", self.on_canvas_configure_client)

        # Adiciona um frame para o conteúdo
        self.frame_conteudo = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_conteudo, anchor="nw")

        self.btn_assinar = tk.Button(
            self.tela, text="Adicionar Cliente", command=self.adicionarCliente
        )
        self.btn_assinar.pack(pady=5)

        self.btn_assinar = tk.Button(
            self.tela, text="Tela Sensores", command=self.abrirTelaSensores
        )
        self.btn_assinar.pack(pady=5)

        # self.lbl_mensagens = tk.Label(self.frame_conteudo, text="Mensagens:")
        # self.lbl_mensagens.pack(pady=5)

        # self.lbl_mensagens_recebidas = tk.Label(self.frame_conteudo, text="")
        # self.lbl_mensagens_recebidas.pack()

        self.tela.mainloop()

    def on_canvas_configure_client(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure_sensor(self, event):
        self.canvas2.configure(scrollregion=self.canvas2.bbox("all"))


if __name__ == "__main__":
    app = Aplicacao()
    app.run()
