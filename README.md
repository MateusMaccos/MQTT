<h1 align="center">
════╡MQTT╞════
</h1>

<img align="center" src="/images/restaum.gif">

## 📚 Resumo
> O protocolo MQTT (Message Queuing Telemetry Transport) é um padrão de comunicação leve e eficiente para troca de mensagens entre dispositivos conectados em redes de Internet das Coisas (IoT). Ele foi projetado para ser simples, fácil de implementar e consumir pouca largura de banda.
- Aplicativo responsivo para Desktop 

# Recursos Principais:

**Objetivo:** Implementação uma rede de Sensores trocando informações com Clientes em um
ambiente IoT simulado
É possível instanciar diversos sensores sendo que cada Sensor tem as seguintes
características:
1) Monitorar apenas um parâmetro (temperatura, umidade ou velocidade)
2) Modificar o valor da leitura atual dos parâmetros
3) Definir limites máximo e mínimo para cada parâmetro
4) Ao se atingir esses limites os sensores enviam uma mensagem para o Broker para o
respectivo tópico relativo ao sensor monitorado.

É possível instanciar diversos Clientes sendo que cada Cliente tem as seguintes
características:
1) Ler os tópicos disponíveis no Broker para cada Sensor e listar as opções disponíveis
2) Permitir escolher quais tópicos “assinar”
3) Apresentar para o usuário as mensagens que chegam para os tópicos escolhidos,
indicando o Sensor que gerou e o valor da leitura realizada.

# Tecnologias Utilizadas:

<img align="center" alt="Python" height="30" width="30" src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/935px-Python-logo-notext.svg.png"> **Tkinter:** É uma biblioteca padrão do Python que oferece uma ampla gama de componentes e recursos para o desenvolvimento de interfaces gráficas. Com o Tkinter, é possível criar janelas, botões, caixas de texto, listas, entre outros elementos interativos que facilitam a interação do usuário com o programa.

<img align="center" alt="Python" height="30" width="30" src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/935px-Python-logo-notext.svg.png"> **Python:** É uma linguagem de programação de alto nível, interpretada e de propósito geral. Ela foi criada por Guido van Rossum e lançada pela primeira vez em 1991. Python possui uma sintaxe simples e legível, o que a torna uma linguagem muito popular entre desenvolvedores de todos os níveis de experiência.

---

