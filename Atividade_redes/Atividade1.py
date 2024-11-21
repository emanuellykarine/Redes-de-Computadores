# realiza and entre o Ip e a máscara
def end_rede(end_ip, end_masc):
    ip_octetos = end_ip.split('.')
    masc_octetos = end_masc.split('.')
    resultado = [
        str(int(ip_octeto) & int(masc_octeto))  # AND bit a bit
        for ip_octeto, masc_octeto in zip(ip_octetos, masc_octetos)
    ]
    return '.'.join(resultado)

# retorna se de fato o endereço de rede de ambos IPS são iguais.
def rede(end_rede_ip1, end_rede_ip2):
    sub1 = end_rede_ip1.split('.')
    sub2 = end_rede_ip2.split('.')
    cont = 0
    for i in range(0,4):
        if sub1[i] == sub2[i]:
            continue
        else:
            return False
    return True

enderecoIp1 = input("Digite o primeiro endereço IP: ")
enderecoIp2 = input("Digite o segundo endereço IP: ")
mascara     = input("Digite a máscara: ")

end_rede_ip1 = end_rede(enderecoIp1, mascara)
end_rede_ip2 = end_rede(enderecoIp2, mascara)

resultado = rede(end_rede_ip1, end_rede_ip2)

if (resultado==True):
    print("Estão na mesma rede")
else:
    print("Não estão na mesma rede")