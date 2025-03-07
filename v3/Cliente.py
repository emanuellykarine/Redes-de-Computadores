import socket # cria a conexão
import time
import json
from Sistema import Sistema

class Cliente:
    def __init__(self) -> None:
        self.server_ip = self.descobrir_servidor()
        self.server_port = 5551

    def descobrir_server(self) -> None:
        # envia um broadcast para encontrar um servidor na rede
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_socket.settimeout(3)  # Timeout de 3 segundos para resposta
        try:
            udp_socket.sendto(b"DISCOVERY", ("255.255.255.255", 5552))  # Broadcast na rede
            msg, server_addr = udp_socket.recvfrom(1024)  # Aguarda resposta
            if msg.decode("utf-8") == "SERVER":
                print(f"Servidor encontrado em {server_addr[0]}")
                return server_addr[0]
        except socket.timeout:
            print("Nenhum servidor encontrado.")
            exit(1)
        finally:
            udp_socket.close()
            
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

