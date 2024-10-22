  # Padrões e Arquitetura de Redes
  - Interoperabilidade => operar em diferentes dispositivos; <br>
  - Endereço MAC => endereço de mundo real, endereço final; <br>
  - Endereço IP => endereço mundo virtual; <br>
  comandos do dia:
  ipcongif => mostra todos os ips possiveis
  route print => todas rotas do computador

    Camadas:
    > Implementa um conjunto de funcionalidades; <br>
    > Liga a interface ao sistema e o sistema ao banco de dados (Sistema complexo); <br> 
    > Protocolos permitem que uma "entidade", de uma camada, em um host, interaja com outro com a mesma camada de outro host (EX: pesquisa http)<br>

- Protocolo ISO: <br> 
  > 7 camadas, cada uma com uma única função <br>
- Internet TCP/IP ==> funde alguns funções de camadas ISO em uma só: <br>
  > 5 camadas (Aplicação e apresentação viraram uma só, <br>
  > No enlace => portal de entrada que precisa do endereço MAC da placa de rede <br>
  > rede(transformar os dados em 0e1),  onde acontece o roteamentos, ver para onde o dado será enviado <br>

