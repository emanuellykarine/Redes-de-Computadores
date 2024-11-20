
def ip_binario(ip):
    octeto = ip.split('.') # Dividi o ip em octetos
    ip_bin = [format(int(octet),'08b') for octet in octeto]
    return '.'.join(ip_bin)

def end_rede(end_ip, end_masc):
    ip_octeto = end_ip.split('.')
    masc_octeto = end_masc.split('.')
    resultado = [str(int(ip_octeto) & int(masc_octeto)) for ip_octeto, masc_octeto in zip(ip_octeto, masc_octeto)]
# função zip emparelha  os elementos 
    return  '.'.join(resultado)


def rede(end_rede_ip1, end_rede_ip2):
    sub1 = end_rede_ip1.split('.')
    sub2 = end_rede_ip2.split('.')
    cont = 0
    for i in range(0,4):
        if sub1[i] == sub2[i]:
            cont += 1
    if cont==3:
        return True
    else:
        return False

enderecoIp1 = input("Digite o primeiro endereço IP: ")
enderecoIp2 = input("Digite o segundo endereço IP: ")
mascara = input("Digite o endereço da Máscara: ")


enderecoIp1 = ip_binario(enderecoIp1)
enderecoIp2 = ip_binario(enderecoIp2)
mascara = ip_binario(mascara)

end_rede_ip1 = end_rede(enderecoIp1, mascara)
end_rede_ip2 = end_rede(enderecoIp2, mascara)

resultado = rede(end_rede_ip1, end_rede_ip2)
if (resultado==True):
    print("Estão na mesma rede")
else:
    print("Não estão na mesma rede")