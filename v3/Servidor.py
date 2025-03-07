import socket
import json
import threading
from Sistema import Sistema

class Servidor:
    def __init__(self) -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Cria o socket utilizando IPv4 (protocolo de endereço) e TCP (tipo do socket)
        self.s.bind(("0.0.0.0", 5551)) #Socket vinculado a um endereço Ip e porta 0.0.0.0 é por que o servidor aceita conexão em qualquer rede
        self.s.listen(5) #maximo 5 conexões
        self.info = {}

        # socket udp para responder os broadcasts
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.udp_socket.bind(("0.0.0.0", 5552))  # Porta para descoberta
        

    def ligar(self) -> None:
        print("Servidor escutando conexões...")
        threading.Thread(target=self.responder_broadcast, daemon=True).start() # thread para responder aos broadcasts
        threading.Thread(target=self.menu, daemon=True).start() # inciia uma thread do menu em paralelo 
        while True:
            clientsocket, address = self.s.accept() #Quando a conexão é aceita ela retorna o socket de comunicação e o endereço ip
            print(f"Conexao estabelecida com {address}.")
            threading.Thread(target=self.receber_dados, args=(clientsocket, address)).start()
            
            
            
    def receber_dados(self, clientsocket, address):
        try:
            msg = clientsocket.recv(1024).decode("utf-8")

            try:
                # Tenta carregar os dados como JSON
                dados_recebidos = json.loads(msg)

                # Salva as informações do cliente
                self.info[address[0]] = {
                    'espaco_livre_hd': dados_recebidos.get("espaco_livre_hd", "Desconhecido"),
                    'qtd_processadores': dados_recebidos.get("qtd_processadores", "Desconhecido"),
                    'espaco_memoria': dados_recebidos.get("espaco_memoria", "Desconhecido")
                }
                self.salvar_em_json()
                print(f"Dados do IP {address[0]} armazenados.")

            except json.JSONDecodeError:
                print(f"Erro ao decodificar JSON de {address[0]}. Dados recebidos: {msg}")

            clientsocket.close()

        except Exception as e:
            print(f"Erro ao receber dados: {e}")
                
                 
    def coletar_informacoes(self, ip):
        self.info[ip] = {
            'espaco_livre_hd': Sistema.espaco_livre_hd(),
            'qtd_processadores': Sistema.qtd_processadores(),
            'espaco_memoria': Sistema.espaco_memoria()
        }
        self.salvar_em_json()
    
    
    def salvar_em_json(self):
        try:
            dados_salvos = {}
            try:
                with open("informacoes_sistema.json", "r") as file:
                    dados_salvos = json.load(file)
            except FileNotFoundError:
                pass

            dados_salvos.update(self.info)

            with open("informacoes_sistema.json", 'w') as file:
                json.dump(dados_salvos, file, indent=3)

        except Exception as e:
            print(f"Erro ao salvar arquivo JSON: {e}")
    
    def calcular_media(self):
        total_pc = len(self.info)
        if total_pc == 0:
            print("Nenhum dado disponível para calcular a média.")
            return
        total_hd = sum(float(pc["espaco_livre_hd"].split()[0]) for pc in self.info.values())
        total_cpu = sum(int(pc["qtd_processadores"]) for pc in self.info.values())
        total_mem = sum(float(pc["espaco_memoria"].split()[0]) for pc in self.info.values())



        print("\nMédia dos computadores conectados")
        print(f"Espaço livre médio no HD: {total_hd / total_pc:.2f} GB")
        print(f"Quantidade média de processadores: {total_cpu / total_pc:.2f}")
        print(f"Memória RAM livre média: {total_mem / total_pc:.2f} GB")    
        
    def menu(self):
        while True:
            print("\n O que deseja visualizar?")
            print("1. Lista de Ips conectados")
            print("2. Consultar as informações por IP")
            print("3. Calcular média dos dados")
            print("4. Fechar servidor")
            opcao = int(input("Opção: "))
            
            if(opcao == 1):
                self.listar_ips()
            elif(opcao == 2):
                ip = input("Digite o IP desejado: ")
                self.consultar_por_ip(ip)
            elif(opcao == 3):
                self.calcular_media()
            elif(opcao == 4):
                print("Servidor fechado...")
                exit()
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
    server.ligar()

if __name__ == "__main__":
    main()
