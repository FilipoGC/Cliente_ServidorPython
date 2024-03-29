import ssl
from threading import Thread
import re
from socket import *
#Dados do servidor

def client_thread():#cria a funcao thread(para possibilitar a conexao de mais de um cliente ao mesmo tempo)
    HOST = 'localhost'
    PORT = 8455
    serverSocket = socket(AF_INET, SOCK_STREAM)#criando socket do servidor
    serverSocket.bind((HOST, PORT))
    serverSocket.listen(5)
    while True:
        conexao, cliente = serverSocket.accept()
        print ('O servidor esta concetado por', cliente)
        msg = str(conexao.recv(1024),'utf-8')#recebendo mensagem do cliente codficando em utf-8 para manipulacao
        print('Comando {} recebido.'.format(msg))
        nomeTime = re.search('<\w+\W*\w*\s*\w*>',msg)#expressao regular para separar o time desejado para o comando 3
        nomeTime = str(nomeTime)#transforma a varaivel nomeTime em tipo string
        x = len(nomeTime)
        nomeTime = nomeTime[41:] + nomeTime[x:]#exclui os caracteres pela esquerda de acordo com o tamanho da string
        nomeTime = nomeTime[:-3]#exclui os caracteres da direita
        Thread(target=tudo, args = (conexao, HOST, PORT, nomeTime, msg)).start()#thread chama a funcao "tudo" e "leva" as variaveis nomeTime e msg


def tudo(conexao, HOST, PORT, nomeTime, msg):#funcao principal contendo todos os comandos,
    
        while True:
            if msg == '/comandos':
                modifiedMsg = 'Voce pode utlizar os comandos: "/comandos", "/exit", "/lider_brasileirao" e "/brasileirao<nome_do_time>" '
                conexao.send(modifiedMsg.encode('utf-8'))#retorna a resposta ao usuario
                #conexao.close()
            elif msg == '/lider_brasileirao':#Utiliza o html do site globo esporte para coletar informacoes do lider atual
                paginaSocket = socket(AF_INET,SOCK_STREAM)
                host = 'globoesporte.globo.com'
                paginaSocket = ssl.wrap_socket(paginaSocket, ssl_version=ssl.PROTOCOL_SSLv23)
                paginaSocket.connect((host, 443))
                requisicao = 'GET /futebol/brasileirao-serie-a/ HTTP/1.1\r\nHost: {}\r\nKeep-Alive: 115\r\nConnection: keep-alive\r\n\r\n'.format(host)
                paginaSocket.send(requisicao.encode())

                html =''
                while True:
                    dados = paginaSocket.recv(2048)#recebe o html da pagina web
                    html += str(dados, 'utf-8', errors = 'ignore')
                    html = str(html)#transforma o html em string
                    if len(dados)<1:
                        break
                    if ('</html>' in str(dados)):
                        break
                paginaSocket.close()#fecha a conexao com o servidor da pagina web
                
                resultado = re.search('"nome_popular":"\w+","ordem":1', html)#utiliza expressao regular para extrair do html o conteudo desejado
                resultadostr = str(resultado)
                resultadostr = resultadostr[64:] + resultadostr[87:]
                resultadostr = resultadostr[:-13]
                modifiedMsg = 'O atual lider do Brasileirao Serie A 2019 é o: {}'.format(resultadostr)
                modifiedMsg = str(modifiedMsg)
                conexao.send(modifiedMsg.encode('utf-8'))#retorna a resposta ao usuario
                #utiliza o html do site terra para obter iformacoes da posicao dos clubes no brasileirao serie a 2019
            elif msg == '/brasileirao<' + nomeTime + '>':#concatena com o nome do clube desejado juntamente do restante do comando
                paginaSocket = socket(AF_INET,SOCK_STREAM)
                host = 'www.terra.com.br'
                paginaSocket = ssl.wrap_socket(paginaSocket, ssl_version=ssl.PROTOCOL_SSLv23)
                paginaSocket.connect((host, 443))
                requisicao = 'GET /esportes/futebol/brasileiro-serie-a/tabela/ HTTP/1.1\r\nHost: {}\r\nKeep-Alive: 115\r\nConnection: keep-alive\r\n\r\n'.format(host)
                paginaSocket.send(requisicao.encode())

                html =''
                while True:
                    dados = paginaSocket.recv(4096)

                    html += str(dados, 'utf-8', errors = 'ignore')
                    html = str(html)
                    if len(dados)< 1 :
                        break
                    if ('</html>' in str(dados)):
                        break
                paginaSocket.close()
                exp = 'posição">\d+<\/td><td class="main shield"><a href="https:\/\/www.terra.com.br\/esportes\/equipes\/\w+\W*\w+" title="'
                exp += nomeTime#concatena a variavel exp com o clube para remover a expressao desejada utilizando expressao regular
                resultado = re.search(exp, html)#obtem a expressao regular do html
                resultadostr = str(resultado)
                posicao = re.search('>\d+<', resultadostr)
                posicao = str(posicao)
                y = len(posicao)
                posicao = posicao[41:] + posicao[y:]
                posicao = posicao[:-3]
                modifiedMsg = 'O {}, esta na {}ª posicao do Brasileirao Serie A 2019'.format(nomeTime, posicao)
                conexao.send(modifiedMsg.encode('utf-8'))#retorna a resposta ao usuario
            elif msg == '/exit':
                modifiedMsg = 'Conexao fechada'
                conexao.send(modifiedMsg.encode('utf-8'))
                conexao.close()
            else:
                modifiedMsg = 'O comando usado nao é valido!'
                conexao.send(modifiedMsg.encode('utf-8'))
client_thread()#chama a funcao client_thread

