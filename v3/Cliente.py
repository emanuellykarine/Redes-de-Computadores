import socket # cria a conexão
import time
import json
from Sistema import Sistema

class Cliente:
    def __init__(self) -> None:
        self.server_ip = self.descobrir_servidor()
        self.server_port = 5551

    def descobrir_server(self) -> None:
        """Busca uma conexao com um servidor"""
        print("Esperando servidores...")
        HOST = ''              # Endereco IP do Servidor
        PORT = 5005            # Porta que o Servidor esta
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        orig = (HOST, PORT)
        udp.bind(orig)
        while True:
            msg, cliente = udp.recvfrom(1024)
            tupla = eval(msg.decode("utf-8")) # A mensagem recebida vem como uma tupla com ip e porta

            return cliente[0], int(tupla[1]) # Retorna o ip e a porta
    def enviar_info(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.server_ip, self.server_port))

            # Coletar informações do sistema
            dados = {
                "espaco_livre_hd": Sistema.espaco_livre_hd(),
                "qtd_processadores": Sistema.qtd_processadores(),
                "espaco_memoria": Sistema.espaco_memoria()
            }

            # Enviar JSON para o servidor
            s.send(json.dumps(dados).encode("utf-8"))
            print("Informações enviadas ao servidor.")

            s.close()
        except Exception as e:
            print(f"Erro ao conectar ao servidor: {e}")
      


def main():
    cliente = Cliente()
    while True:
        cliente.solicitar_info()
        time.sleep(10)
        cliente.fechar_conexao()

if __name__ == "__main__":
    main()

