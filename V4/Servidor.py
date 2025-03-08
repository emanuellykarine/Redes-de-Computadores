import socket
import json
import threading #Permite a execução de várias funções ao mesmo tempo
import time

class Servidor:
    def __init__(self) -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Cria o socket TCP
        self.s.bind(("0.0.0.0", 5551))  #O servidor aceita conexões em qualquer rede
        self.s.listen(5)  #Máximo de 5 conexões
        self.info = {} #Armazena informações recebidas dos clientes
        self.ipPorta = ("0.0.0.0", 5551)  #Define o IP e a porta para broadcast
        self.publicando = True  #Controla se broadcast UDP está ativo
        self.executando = True  #Controla se o servidor está rodando
        self.recebendo_dados = True #Controla se o servido está aceitando conexões

    def ligar(self) -> None:
        print("Servidor escutando conexões...")
        
        # Inicia a thread para enviar broadcasts
        threading.Thread(target=self.broadcast_server_ip, daemon=True).start()

        # Inicia a thread para capturar entrada do usuário
        threading.Thread(target=self.aguardar_comandos, daemon=True).start()

        while self.executando: #Enquanto o servidor estiver rodando
            try:
                clientsocket, address = self.s.accept()  #Aguarda conexões
                if self.recebendo_dados: #Se o servidor estiver aceitando conexões
                    print(f"Conexão estabelecida com {address}.") #Mostra que a conexão foi estabelecida
                    threading.Thread(target=self.receber_dados, args=(clientsocket, address)).start() #Inicia thread de receber as informações do cliente
                else:
                    clientsocket.close()  #Fecha a conexão se não estiver recebendo dados
            except:
                break  #Se o servidor for interrompido, ele sai do loop

    #Função para obter todos os IPs locais do servidor e enviar o broadcast UDP com seu IP e porta na rede para o cliente encontrar
    def broadcast_server_ip(self):
        """Envia periodicamente o IP e a porta do servidor via broadcast UDP."""
        interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
        allips = [ip[-1][0] for ip in interfaces]  #Obtém todos os IPs do servidor
        msg = str(self.ipPorta).encode("utf-8") #Codifica a mensagem recebida

        while self.executando: #Enquanto o servidor estiver rodando 
            if self.publicando: #Se o broadcast estiver ativo
                for ip in allips:
                    try:
                        print(f'Publicando em {ip}')
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  #Cria socket UDP
                        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  #Habilita broadcast
                        sock.bind((ip, 0))  #Usa o IP da interface
                        sock.sendto(msg, ("255.255.255.255", 5005))  #Envia broadcast
                        sock.close()
                    except Exception as e:
                        print(f"Erro ao enviar broadcast em {ip}: {e}")

                time.sleep(5)  # Espera 5 segundos antes de enviar novamente
            else:
                time.sleep(1)  # Aguarda para evitar loop infinito consumindo CPU

    def aguardar_comandos(self):
        """Espera o usuário digitar comandos no terminal."""
        while self.executando: #Enquanto o servidor estiver rodando aguarda o cliente digitar 4 para parar broadcast
            op = input("\nDigite '4' para parar o broadcast e abrir o menu\n ")
            if op == "4":
                self.publicando = False  #Para o broadcast e só volta quando digitar 4 novamente
                print("\nBroadcast interrompido. Entrando no menu...")
                self.menu() #Vai para o menu
                #self.publicando = True  # Retorna o broadcast automaticamente

    def receber_dados(self, clientsocket, address):
        try:
            msg = clientsocket.recv(1024).decode("utf-8")
            try:
                dados_recebidos = json.loads(msg)
                self.info[address[0]] = {
                    'espaco_livre_hd': dados_recebidos.get("espaco_livre_hd", "Desconhecido"),
                    'qtd_processadores': dados_recebidos.get("qtd_processadores", "Desconhecido"),
                    'espaco_memoria': dados_recebidos.get("espaco_memoria", "Desconhecido"),
                    'temperatura': dados_recebidos.get("temperatura", "Desconhecido")
                }
                self.salvar_em_json()
                if self.recebendo_dados:
                    print(f"Dados do IP {address[0]} armazenados.")
            except json.JSONDecodeError:
                print(f"Erro ao decodificar JSON de {address[0]}. Dados recebidos: {msg}")

            clientsocket.close()
        except Exception as e:
            print(f"Erro ao receber dados: {e}")

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
                json.dump(dados_salvos, file, indent=4)

        except Exception as e:
            print(f"Erro ao salvar arquivo JSON: {e}")

    def menu(self):
            self.recebendo_dados = False #Servidor para de aceitar novas conexões

            while True:
                """Executa uma ação do menu e volta para o broadcast."""
                print("\nO que deseja visualizar?")
                print("1. Lista de IPs conectados")
                print("2. Consultar as informações por IP")
                print("3. Calcular média dos dados")
                print("4. Voltar ao servidor e retomar broadcast")
                
                opcao = input("Opção: ")

                if opcao == "1":
                    self.listar_ips()
                elif opcao == "2":
                    ip = input("Digite o IP desejado: ")
                    self.consultar_por_ip(ip)
                elif opcao == "3":
                    self.calcular_media()
                elif opcao == "4":
                    print("Voltando ao servidor e retomando broadcast...")
                    self.recebendo_dados = True #Servidor volta a aceitar conexões
                    self.publicando = True #Broadcast ativado novamente
                    break
                else:
                    print("Opção inválida!\n")

            

    def listar_ips(self):
        try:
            with open("informacoes_sistema.json", "r") as file:
                dados = json.load(file)
                print("\nIPs que realizaram conexão: ")
                for ip in dados.keys():
                    print(f"- {ip}")
        except FileNotFoundError:
            print("Nenhuma informação registrada ainda.")

    def consultar_por_ip(self, ip):
        try:
            with open("informacoes_sistema.json", "r") as file:
                dados = json.load(file)
                info = dados.get(ip)
                if info:
                    print(f"\n--Informações do IP {ip} --")
                    print(f"Espaço livre HD: {info.get('espaco_livre_hd')}")
                    print(f"Quantidade de processadores: {info.get('qtd_processadores')}")
                    print(f"Espaço livre na memória RAM: {info.get('espaco_memoria')}")
                    print(f"Temperatura do processador: {info.get('temperatura')}")
                else:
                    print(f"O IP não foi encontrado.\n")
        except FileNotFoundError:
            print("Não há informações salvas ainda.\n")

    def calcular_media(self):
        total_pc = len(self.info)
        if total_pc == 0:
            print("Nenhum dado disponível para calcular a média.")
            return
        total_hd = sum(float(pc["espaco_livre_hd"].split()[0]) for pc in self.info.values())
        total_cpu = sum(int(pc["qtd_processadores"]) for pc in self.info.values())
        total_mem = sum(float(pc["espaco_memoria"].split()[0]) for pc in self.info.values())
        total_temperatura = sum(int(pc["temperatura"].split("°")[0]) for pc in self.info.values())

        print("\n--Média dos computadores conectados--")
        print(f"Espaço livre no HD: {total_hd / total_pc:.2f} GB")
        print(f"Quantidade de processadores: {total_cpu / total_pc:.2f}")
        print(f"Memória RAM livre: {total_mem / total_pc:.2f} GB")  
        print(f"Temperatura: {total_temperatura / total_pc:.2f}°C")

def main():
    server = Servidor()
    try:
        server.ligar()
    except KeyboardInterrupt:
        print("\nEncerrando servidor...")
        server.executando = False  # Para todas as threads
        server.s.close()

if __name__ == "__main__":
    main()
