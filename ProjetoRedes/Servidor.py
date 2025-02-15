# Essa estrutura permite que o servidor:
#   Receba um comando de um cliente.
#   Processe o comando usando a classe Sistema.
#   Envie a resposta de volta para o cliente.
#   Feche a conexão, ficando pronto para atender o próximo cliente.
import socket, time
from ProjetoRedes.Sistema import Sistema
from threading import Thread

class Servidor:
    soc : socket
    sis = Sistema()
    def __init__(self, ip:str, porta:int) -> None:
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria um socket TCP para comunicação
        self.ipPorta = (ip, porta)
        self.soc.bind(self.ipPorta)

    
    def ligar(self) -> None:
        self.soc.listen() # aguarda comunicação
        publicador = Thread(target=self.publicarCoiso()) # thread iniciada para o metodo publicacoiso anunciando o servidor na rede
        publicador.start()
        publicador.setblocking(False)
        while True:
            cliente, address = self.soc.accept()
            msg = cliente.recv(128).decode("utf-8") # o servidor recebe o comando que irá executar
            retorno = str(self.sis.comando(msg)) # vai interpretar o comando e executar a ação correspondente de acordo com o que foi digitado pelo cliente
            print("retorno: ", retorno)
            cliente.send(bytes(retorno,"utf-8")) #  a string é convertida para bytes usando a codificação utf-8 e enviada para o cliente
            cliente.close() # o cliente recebe a resposta e o servidor é fehcado
    
    def publicarCoiso(self) -> None:
        interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
        allips = [ip[-1][0] for ip in interfaces]
        msg = str(self.ipPorta).encode("utf-8")
        while True:
            for ip in allips:
                print(f'Publicando em {ip}')
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.bind((ip,0))
                sock.sendto(msg, ("255.255.255.255", 5005))
                sock.close()
            time.sleep(60)

def main():
    server = Servidor("0.0.0.0",8888)
    server.ligar()

if __name__ == "__main__":
    main()
        