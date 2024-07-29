import tkinter as tk
import paho.mqtt.client as mqtt
import threading
import time
from tkinter import ttk


class Sensor:
    def __init__(self, nome):
        self.nome = nome
        self.ativo = False
        self.parametro = None
        self.min = None
        self.max = None
        self.valor_atual = None
        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION1,
        )
        self.client.connect(host="test.mosquitto.org", port=1883)
        self.client.loop_start()

    def desativar(self):
        self.ativo = False

    def iniciar_leituras(self):
        self.ativo = True
        while self.ativo:
            if self.valor_atual != None:
                mensagem = str(self.valor_atual)
                if self.min not in [None, ""] or self.max not in [None, ""]:
                    if self.valor_atual == self.min:
                        mensagem += " (MIN)"
                    elif self.valor_atual == self.max:
                        mensagem += " (MAX)"
                    elif self.valor_atual > self.max:
                        mensagem += " (>MAX)"
                    elif self.valor_atual < self.min:
                        mensagem += " (<MIN)"
                self.client.publish(
                    topic=self.nome,
                    payload=mensagem + f" de {self.parametro}",
                )
                time.sleep(1)

    def set_valor_atual(self):
        if self.campo_valor_atual.get() not in [None, ""]:
            self.valor_atual = float(self.campo_valor_atual.get())
        else:
            print("Digitou nada")

    def set_valor_min(self):
        if self.campo_valor_min.get() not in [None, ""]:
            self.min = float(self.campo_valor_min.get())
        else:
            print("Digitou nenhum minimo")

    def set_valor_max(self):
        if self.campo_valor_max.get() not in [None, ""]:
            self.max = float(self.campo_valor_max.get())
        else:
            print("Digitou nenhum maximo")

    def set_parametro(self):
        self.parametro = self.parametro_selecionado.get()

    def desenhar_painel(self, tela):
        self.tela_sensor = ttk.LabelFrame(tela, text="Sensor", padding=(10, 10))
        self.tela_sensor.pack(pady=5)

        frame_config = tk.Frame(self.tela_sensor)
        frame_config.pack(pady=5)

        self.lbl_cliente = tk.Label(frame_config, text=self.nome)
        self.lbl_cliente.pack(padx=20, side=tk.LEFT)

        self.lbl_cliente_status = tk.Label(
            frame_config, text=f'Status: {"Ativado" if self.ativo else "Desativado"}'
        )
        self.lbl_cliente_status.pack(padx=20, side=tk.LEFT)

        self.frame_param_valor = tk.Frame(frame_config)
        self.frame_param_valor.pack(padx=10, side=tk.LEFT)

        self.lbl_parametro = tk.Label(self.frame_param_valor, text="Parâmetro: ")
        self.lbl_parametro.pack(padx=20)

        opcoes = ["Temperatura", "Umidade", "Velocidade"]
        if self.parametro not in [None, ""]:
            opcao_inicial = self.parametro
        else:
            opcao_inicial = opcoes[0]

        self.parametro_selecionado = tk.StringVar(value=opcoes)

        self.dropdown = ttk.OptionMenu(
            self.frame_param_valor, self.parametro_selecionado, opcao_inicial, *opcoes
        )
        self.dropdown.pack(pady=15)

        self.lbl_cliente = tk.Label(self.frame_param_valor, text="Valor Atual: ")
        self.lbl_cliente.pack(padx=20)

        self.campo_valor_atual = tk.Entry(self.frame_param_valor)
        if self.valor_atual != None:
            self.campo_valor_atual.insert(tk.END, self.valor_atual)
        self.campo_valor_atual.pack(pady=20)

        self.frame_min_max = tk.Frame(frame_config)
        self.frame_min_max.pack(padx=20, side=tk.RIGHT)

        self.lbl_cliente = tk.Label(self.frame_min_max, text="Valor Mínimo: ")
        self.lbl_cliente.pack(padx=20)

        self.campo_valor_min = tk.Entry(self.frame_min_max)
        if self.min != None:
            self.campo_valor_min.insert(tk.END, self.min)
        self.campo_valor_min.pack(pady=20)

        self.lbl_cliente = tk.Label(self.frame_min_max, text="Valor Máximo: ")
        self.lbl_cliente.pack(padx=20)

        self.campo_valor_max = tk.Entry(self.frame_min_max)
        if self.max != None:
            self.campo_valor_max.insert(tk.END, self.max)
        self.campo_valor_max.pack(pady=20)

        separator = tk.Frame(self.tela_sensor, height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill="x", padx=5, pady=5, side=tk.BOTTOM)


class Aplicacao:
    def __init__(self):
        self.sensores = []
        self.tela = None
        self.telaSensores = None
        self.tema = "dark"
        self.sensores_mqtt = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION1,
        )
        self.sensores_mqtt.connect(host="test.mosquitto.org", port=1883)
        self.sensores_mqtt.loop_start()

    def mudarTema(self):
        if self.tema == "dark":
            self.tema = "light"
        else:
            self.tema = "dark"
        self.telaSensores.tk.call("set_theme", self.tema)

    def adicionarSensor(self):
        sensor = Sensor(f"sensor/{len(self.sensores) + 1}")
        self.sensores.append(sensor)
        sensor.desenhar_painel(self.frame_sensores)
        self.sensores_mqtt.publish(
            topic="sensor/qntd",
            payload=f"{len(self.sensores)}",
        )

    def atualizarSensores(self):
        for sensor in self.sensores:
            sensor.set_valor_atual()
            sensor.set_valor_min()
            sensor.set_valor_max()
            sensor.set_parametro()
            sensor.tela_sensor.destroy()
            thread_envio = threading.Thread(target=sensor.iniciar_leituras, daemon=True)
            thread_envio.start()
            sensor.desenhar_painel(self.frame_sensores)

    def desativarSensores(self):
        for sensor in self.sensores:
            sensor.desativar()
            sensor.tela_sensor.destroy()
            sensor.desenhar_painel(self.frame_sensores)

    def abrirTelaSensores(self):
        self.telaSensores = tk.Tk()
        self.telaSensores.title("Sensores MQTT")
        self.telaSensores.geometry("1000x500")
        self.telaSensores.iconbitmap("imagens/iconeSensor.ico")
        self.telaSensores.tk.call("source", "azure.tcl")
        self.telaSensores.tk.call("set_theme", self.tema)

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

        self.frame_botoes = ttk.LabelFrame(
            self.telaSensores, text="Configuração", padding=(10, 10)
        )
        self.frame_botoes.pack(padx=5)

        self.btn_add_sensor = ttk.Button(
            self.frame_botoes,
            text="Adicionar sensores",
            style="Accent.TButton",
            command=self.adicionarSensor,
        )
        self.btn_add_sensor.pack(padx=5, pady=10, side=tk.TOP)

        self.btn_atualizar_dados = ttk.Button(
            self.frame_botoes, text="Ativar sensores", command=self.atualizarSensores
        )
        self.btn_atualizar_dados.pack(
            padx=5,
        )

        self.btn_desativar_sensores = ttk.Button(
            self.frame_botoes, text="Desativar sensores", command=self.desativarSensores
        )
        self.btn_desativar_sensores.pack(
            padx=5,
            pady=10,
        )

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

        self.telaSensores.mainloop()

    def on_canvas_configure_sensor(self, event):
        self.canvas2.configure(scrollregion=self.canvas2.bbox("all"))


if __name__ == "__main__":
    app = Aplicacao()
    app.abrirTelaSensores()
