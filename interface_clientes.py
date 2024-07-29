import tkinter as tk
import paho.mqtt.client as mqtt
from tkinter import ttk


class Sensor:
    def __init__(self, nome):
        self.nome = nome


class Cliente:
    def __init__(self, id):
        self.id = id
        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION1,
        )
        self.client.on_message = self.on_message
        self.client.connect(host="test.mosquitto.org", port=1883)
        self.client.loop_start()

        self.opcoes_disponiveis = []
        self.opcoes_selecionadas = []

    def desenhar_painel(self, tela, opcoes_disponiveis):
        tela_cliente = ttk.LabelFrame(tela, text="Cliente", padding=(10, 10))
        tela_cliente.pack(pady=5, padx=5)

        frame_config = tk.Frame(tela_cliente)
        frame_config.pack(pady=5)

        self.lbl_cliente = tk.Label(frame_config, text=f"ID: {self.id}")
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

        frame_caixa_mensagens = tk.Frame(frame_mensagens)
        frame_caixa_mensagens.pack(fill=tk.BOTH, expand=True)

        self.lb_mensagens = tk.Listbox(frame_caixa_mensagens, width=50, height=10)
        self.lb_mensagens.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Crie uma barra de rolagem
        scrollbar = tk.Scrollbar(
            frame_caixa_mensagens, orient=tk.VERTICAL, command=self.lb_mensagens.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Vincule a barra de rolagem ao Listbox
        self.lb_mensagens.config(yscrollcommand=scrollbar.set)

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

        self.btn_assinar = ttk.Button(
            frame_btn, text="Assinar", style="Accent.TButton", command=self.assinar
        )
        self.btn_assinar.pack(pady=(75, 0))

        self.btn_tirar_assinatura = ttk.Button(
            frame_btn, text="Remover assinatura", command=self.removerAssinatura
        )
        self.btn_tirar_assinatura.pack(pady=20)

        separator = tk.Frame(tela_cliente, height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill="x", padx=5, pady=5, side=tk.BOTTOM)

    def on_message(self, client, userdata, message):
        self.lb_mensagens.insert(0, f"{message.topic} mediu {message.payload.decode()}")

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
        self.sensores_mqtt = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION1,
        )
        self.sensores_mqtt.on_message = self.verificar_sensores_criados
        self.sensores_mqtt.connect(host="test.mosquitto.org", port=1883)
        self.sensores_mqtt.loop_start()
        self.sensores_mqtt.subscribe("sensor/qntd")

        self.sensores = []
        self.clientes = []
        self.tela = None
        self.telaSensores = None
        self.tema = "dark"

    def mudarTema(self):
        if self.tema == "dark":
            self.tema = "light"
        else:
            self.tema = "dark"
        self.tela.tk.call("set_theme", self.tema)

    def adicionarSensor(self):
        sensor = Sensor(f"sensor/{len(self.sensores) + 1}")
        self.sensores.append(sensor)
        # Atualiza as opções disponíveis em todos os clientes
        for cliente in self.clientes:
            cliente.atualiza_lista_sensores(sensor)

    def verificar_sensores_criados(self, client, userdata, message):
        diferencaDeQuantidade = int(message.payload.decode()) - len(self.sensores)
        if diferencaDeQuantidade > 0:
            for _ in range(diferencaDeQuantidade):
                self.adicionarSensor()

    def adicionarCliente(self):
        cliente = Cliente(len(self.clientes) + 1)
        self.clientes.append(cliente)
        cliente.desenhar_painel(self.frame_conteudo, self.sensores)

    def run(self):
        self.tela = tk.Tk()
        self.tela.title("Clientes MQTT")
        self.tela.geometry("1200x500")
        self.tela.iconbitmap("imagens/iconeCliente.ico")
        self.tela.tk.call("source", "azure.tcl")
        self.tela.tk.call("set_theme", "dark")

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

        self.frame_botoes = ttk.LabelFrame(
            self.telaSensores, text="Configuração", padding=(10, 10)
        )
        self.frame_botoes.pack(padx=5)

        self.btn_assinar = ttk.Button(
            self.frame_botoes,
            text="Adicionar Cliente",
            style="Accent.TButton",
            command=self.adicionarCliente,
        )
        self.btn_assinar.pack(pady=5, padx=10)

        self.switch = ttk.Checkbutton(
            self.frame_botoes,
            text="Tema",
            style="Switch.TCheckbutton",
            command=self.mudarTema,
        )
        self.switch.pack(
            padx=5,
            pady=10,
        )

        self.tela.mainloop()

    def on_canvas_configure_client(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure_sensor(self, event):
        self.canvas2.configure(scrollregion=self.canvas2.bbox("all"))


if __name__ == "__main__":
    app = Aplicacao()
    app.run()
