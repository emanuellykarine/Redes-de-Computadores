import socket
HOST = 'localhost'  # Endereco IP do Servidor --> Vai receber só na porta que ele quer, se tirar isso aqui e deixar vazio ele recebe em qualquer porta
PORT = 5000            # Porta que o Servidor esta
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORT)
msg = "Mensagem!!"
udp.sendto (msg.encode(), dest)
udp.close()