import socket
import json
from Sistema import Sistema

class Servidor:
    def __init__(self) -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Cria o socket utilizando IPv4 (protocolo de endereço) e TCP (tipo do socket)
        self.s.bind(("0.0.0.0", 5551)) #Socket vinculado a um endereço Ip e porta 0.0.0.0 é por que o servidor aceita conexão em qualquer rede
        self.s.listen(5) #maximo 5 conexões
        self.info = {}

    def ligar(self) -> None:
        while True:
            clientsocket, address = self.s.accept() #Quando a conexão é aceita ela retorna o socket de comunicação e o endereço ip
            print(f"Conexao estabelecida com {address}.")
            msg = clientsocket.recv(1024).decode("utf-8") #Recebe a mensagem do cliente em até 1024 bytes

            if msg == "get_info":
                self.coletar_informacoes(address[0]) # mandando o ip para salvar em informacoes_sistema
                # self.coletar_informacoes(f"{address[0]}:{address[1]}") se colocar a porta ele vai diferenciar 
            else:
                clientsocket.send(b"Comando invalido")
                
            self.menu() # mostra o menu

    def enviar_broadcast(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto("Servidor está aberto para conexões!", ("255.255.255.255", self.porta))
        sock.close()

    def coletar_informacoes(self, ip) -> str:
        self.info[ip] = {
            'espaco_livre_hd': Sistema.espaco_livre_hd(),
            'qtd_processadores': Sistema.qtd_processadores(),
            'espaco_memoria': Sistema.espaco_memoria()
        # self.info['temperatura'] = Sistema.temperatura()
        }
        # Salva as informações no arquivo JSON
        self.salvar_em_json()

        
    def salvar_em_json(self):
        try: 
            dados_salvos = {}
            try:# vai atualizar o arquivo com as informações caso já tenha inforamções presentes caso exista
                with open("informacoes_sistema.json", "r") as file: # r = read
                    dados_salvos = json.load(file)
            except FileNotFoundError:
                pass
            
            dados_salvos.update(self.info)
            
            with open("informacoes_sistema.json", 'w') as file:
                    json.dump(self.info, file, indent=3)
        except Exception as e:
            print(f"Erro ao salvar arquivo JSON: {e}")
          
        
    def menu(self):
        while True:
            print("\n O que deseja visualizar?")
            print("1. Lista de Ips conectados")
            print("2. Consultar as informações por IP")
            print("3. Fechar servidor")
            opcao = int(input("Opção: "))
            
            if(opcao == 1):
                self.listar_ips()
            elif(opcao == 2):
                ip = input("Digite o IP desejado: ")
                self.consultar_por_ip(ip)
            elif(opcao == 3):
                print("Servidor fechado...")
                break
            else:
                print("Opcao inválida!\n") 
                
                
    def listar_ips(self):
        try:
            with open("informacoes_sistema.json", "r") as file:
                dados = json.load(file)
                print("\nIps que realizaram conexão: ")
                for ip in dados.keys():
                    print(f"- {ip}")
        except FileNotFoundError:
            print("Nenhuma informação registrada ainda")
            
            
    def consultar_por_ip(self,ip):
        try:
            with open("informacoes_sistema.json", "r") as file:
                dados = json.load(file)
                info = dados.get(ip)
                if info:
                    print(f"\nInformações do IP {ip}: ")
                    print(f"Espaço livre HD: {info.get('espaco_livre_hd')}")
                    print(f"Quantidade de processadores: {info.get('qtd_processadores')}")
                    print(f"Espaço livre na mem RAM: {info.get('espaco_memoria')}")
                else:
                    print(f"O IP não encontrado\n")
        except FileNotFoundError:
            print("Não informações salvas ainda\n")
    
    
def main():
    server = Servidor()
    server.enviar_broadcast()
    server.ligar()

if __name__ == "__main__":
    main()
