from socket import *
#dados do cliente para conexao com servidor
HOST = 'localhost'
PORT = 8455
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((HOST, PORT))
print ('Conexao Estabelecida')
#recebe resposta do servidor, e envia comandos
while True:
    msg = input('Digite o comando desejado: ')#le o comando do cliente
    clientSocket.send(msg.encode('utf-8'))#envia o comando para o servidor usando utf-8
    modifiedMsg = str(clientSocket.recv(1024),'utf-8')#recebe o comando do servidor
    print('Mensgaem do servidor: {}'.format(modifiedMsg))
    print('Reeinicie o Servidor e o Cliente')
    break


