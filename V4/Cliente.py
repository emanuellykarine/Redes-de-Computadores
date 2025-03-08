import socket  # Cria a conexão
import time
import json
import ast  # Importando para segurança na avaliação de tupla
from Sistema import Sistema 

class Cliente:
    def __init__(self) -> None:
        self.server_ip, self.server_port = self.descobrir_servidor()

    def descobrir_servidor(self) -> tuple: #Retorna uma tupla com o ip e a porta
        """Busca uma conexão com um servidor"""
        print("Esperando servidores...")
        HOST = ''              # Endereço IP do Servidor
        PORT = 5005            # Porta que o Servidor está
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Conexão UDP
        orig = (HOST, PORT)
        udp.bind(orig) #Associa o socket a porta 5005

        while True:
            msg, cliente = udp.recvfrom(1024) #Espera uma mensagem do servidor
            tupla = ast.literal_eval(msg.decode("utf-8"))  # Usando ast.literal_eval converte string para tupla

            return cliente[0], int(tupla[1])  # Retorna o ip e a porta como tupla (str, int)
          
    def enviar_info(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Cria socket TCP
            s.connect((self.server_ip, self.server_port)) #Conecta ao servidor

            # Coletar informações do sistema
            dados = {
                "espaco_livre_hd": Sistema.espaco_livre_hd(),
                "qtd_processadores": Sistema.qtd_processadores(),
                "espaco_memoria": Sistema.espaco_memoria(),
                "temperatura": Sistema.temperatura()
            }

            # Serializar o dicionário para JSON e depois para bytes
            dados_json = json.dumps(dados)  # Converte o dicionário para uma string JSON
            s.send(dados_json.encode("utf-8"))  # Converte a string JSON para bytes e envia ao servidor
            print("Informações enviadas ao servidor.")

            s.close()  # Fechar a conexão depois de enviar os dados
        except Exception as e:
            print(f"Erro ao conectar ao servidor: {e}")
            

def main():
    cliente = Cliente() #Cria um cliente e descobre o servidor
    while True:
        cliente.enviar_info()  # Enviar informações do sistema para o servidor
        time.sleep(10)  # Aguardar 10 segundos antes de enviar novamente


if __name__ == "__main__":
    main()
