import socket #Utilizado para criar conexões de rede

class Cliente:
    def __init__(self) -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Cria o socket utilizando IPv4 (protocolo de endereço) e TCP (tipo do socket)
        self.s.connect(("255.255.255.255", 5551)) #Conecta o socket à máquina local na porta 5551
        self.s.bind("0.0.0.0", 5551)
        
    def solicitar_info(self) -> None:
        # Envia um comando fixo para o servidor solicitar as informações do sistema
        self.s.send(b"get_info")

    def fechar_conexao(self) -> None:
        self.s.close()

def main():
    cliente = Cliente()
    cliente.solicitar_info()
    cliente.fechar_conexao()

if __name__ == "__main__":
    main()
