#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Gustavo Fernandes dos Santos
# Email: gfdsantos@inf.ufpel.edu.br
# versão 0.9

from datetime import datetime
from subprocess import call
from calendar import monthrange
import os
import sys

# Valores default
INTERVALO = 30
MIN_SUP = 30
MIN_INF = 0
MODO = "topo"

GOES_topo = "http://www.inmet.gov.br/projetos/cga/capre/sepra/GEO/GOES12/AMERICA_SUL/AS12_TN"
GOES_visivel = "http://www.inmet.gov.br/projetos/cga/capre/sepra/GEO/GOES12/AMERICA_SUL/AS12_VI"
GOES_infravermelho = "http://www.inmet.gov.br/projetos/cga/capre/sepra/GEO/GOES12/AMERICA_SUL/AS12_IV"
GOES_vapor = "http://www.inmet.gov.br/projetos/cga/capre/sepra/GEO/GOES12/AMERICA_SUL/AS12_VA"

# Função que imprime as informações do desenvolvedor
def imprimir_informacoes():
	"""
	Imprime as informaçoes do desenvolvedor
	"""
	call(["clear"])
	print("[*] Baixador de imagens do INMET. v0.9")
	print("[*] Autor: Gustavo Fernandes dos Santos")
	print("[*] Email: gfdsantos@inf.ufpel.edu.br")
	print("    -----------------------------------")
	print("[!] Imagens são produto do GOES - América Latina - Topo das núvens")
	print("                                                   Visível")
	print("                                                   Infravermelho termal")
	print("                                                   Vapor d'Agua")
	print("    -----------------------------------")


# 
def print_uso_batch():
	#call(["clear"])
	print("""[*] Modo de uso em batch:
    $ ./baixar_goes.py <lista de argumentos>

    Os argumentos do programa são processados por um parser, configurando os parâmetros do 
    script.

    Modos de configuração:
        -n_imagens  <seguido de um número inteiro que representa o número de imagens para
                     serem baixadas.

        -modo       <seguido de uma palavra que indica qual tipo de imagens serão baixadas do
                     satélite GOES. As opções são:
                         topo           |  Serão baixadas imagens de topo das núvens
                         visivel        |  Serão baixadas imagens da banda visível
                         infravermelho  |  Serão baixadas imagens da banda infravermelho termal
                         vapor          |  Serão baixadas imagens da banda de vapor d'agua

    Exemplo de execução:
    $ ./get_images.py -n_imagens 3 -modo vapor

    [*] Baixador de imagens do INMET. v0.72
    [*] Autor: Gustavo Fernandes dos Santos
    [*] Email: gfdsantos@inf.ufpel.edu.br
        -----------------------------------
    [!] Imagens são produto do GOES - América Latina - Topo das nuvens
                                                       Visível
                                                       Infravermelho termal
                                                       Vapor d'Agua
        -----------------------------------
    [!] Estabelecendo conexao...
    [+] Online
    [+] Gerando links...
    [!] Testando o link:
    
    http://www.inmet.gov.br/projetos/cga/capre/sepra/GEO/GOES12/AMERICA_SUL/AS12_VA201607272000.jpg
    [+] Link ok.
    [!] Testando o link:
    
    http://www.inmet.gov.br/projetos/cga/capre/sepra/GEO/GOES12/AMERICA_SUL/AS12_VA201607271930.jpg
    [+] Link ok.
    [!] Testando o link:
    
    http://www.inmet.gov.br/projetos/cga/capre/sepra/GEO/GOES12/AMERICA_SUL/AS12_VA201607271900.jpg
    [+] Link ok.
    [+] Baixando imagens...

    AS12_VA201607272000.jpg 100%[==========================================>] 120,63K   129KB/s    in 0,9s
    AS12_VA201607271930.jpg 100%[==========================================>] 120,03K   124KB/s    in 1,0s
    AS12_VA201607271900.jpg 100%[==========================================>] 119,16K   148KB/s    in 0,8s    
    [!] Tentando criar o diretório "imagens"
    [!] O diretório já existe.
    [!] Movendo imagens...
    [+] Ok.
    [+] Pronto.""")


def print_erro():
	print("[-] Erro na inicializaçao.")
	print("[!] Execute novamente utilizando como argumento \"ajuda\".")
	print("[!] Exemplo: $ ./get_imagens.py ajuda")


def testa_conexao():
	print("[!] Estabelecendo conexao...")
	programa = """wget -q --spider http://www.inmet.gov.br

					if [ $? -eq 0 ]; then
    					echo "[+] Online"
					else
    					echo "[-] Offline"
					fi"""

	script = open("script.sh", "w")
	script.write(programa)
	script.close()
	res = call(["sh", "script.sh"])
	call(["rm", "script.sh"])
	if res == "[-] Offline":
		sys.exit("[-] Sem conexão.")


def imagem_online(link):
	print("[!] Testando o link:")
	print("    " + link)
	c = call(["wget", "-q", "--spider", link])
	if c != 0:
		print("[-] Não foi possível atingir o alvo.")
		return False
	else:
		print("[+] Link ok.")
		return True


# usa o parâmetro de intervalo INTERVALO
def retrocede(ano, mes, dia, hora, minuto):
	minuto = minuto - INTERVALO
	if minuto < 0:
		hora = hora - 1
		if hora < 0:
			hora = hora + 24
			dia = dia - 1
			if dia <= 0:
				mes = mes - 1
				if mes <= 0:
					mes = 1
					ano = ano - 1

				dia = monthrange(ano, mes)
				
		minuto = MIN_SUP
	else:
		minuto = MIN_INF
	return (ano, mes, dia, hora, minuto)


def gerar_links(arg):
	hora = datetime.now().hour
	minuto = datetime.now().minute
	dia = datetime.now().day
	mes = datetime.now().month
	ano = datetime.now().year

	if minuto > 0: minuto = INTERVALO
	else: minuto = 0

	if arg == 0:
		qtd = input("[?] Quantidade de imagens\n ~> ")
	else:
		qtd = arg

	if int(qtd) == 0:
		sys.exit("Ok.")
	elif int(qtd) < 0:
		sys.exit("[!] Inválido. A quantidade de imagens deve ser um número inteiro positivo.")

	print("[+] Gerando links...")

	if MODO == "topo":
		preLink = GOES_topo
	elif MODO == "visivel":
		preLink = GOES_visivel
	elif MODO == "infravermelho":
		preLink = GOES_infravermelho
	elif MODO == "vapor":
		preLink = GOES_vapor

	links = []
	sano = ""
	smes = ""
	sdia = ""
	shora = ""
	sminuto = ""

	i = 0
	t = int(qtd)

	e = 0

	while i < t:
		ano, mes, dia, hora, minuto = retrocede(ano, mes, dia, hora, minuto)

		sano = str(ano)
		if mes < 10: smes = "0" + str(mes)
		else: smes = str(mes)
		if dia < 10: sdia = "0" + str(dia)
		else: sdia = str(dia)
		if hora < 10: shora = "0" + str(hora)
		else: shora = str(hora)
		if minuto < 10: sminuto = "0" + str(minuto)
		else: sminuto = str(minuto)

		link = preLink + sano + smes + sdia + shora + sminuto + ".jpg"

		if imagem_online(link):
			links.append(link)
			e = 0
		else:
			i = i - 1
			e = e + 1
			if e >= 10: 
				print("[-] Verifique a sua conexão, se o INMET está online e")
				print("    se o programa está gerando os links corretos.")
				sys.exit("[!] Saindo...")

		i = i + 1

	return links



def baixar_imagens(links):
	print("[+] Baixando imagens...\n")
	if not os.path.isdir("imagens/"):
		call(["mkdir", "imagens"])

	r = []
	for link in links:
		n = call(["wget", "-q", "--show-progress", link])
		r.append(n)

	return r


def mover_imagens():
	print("[!] Tentando criar o diretório \"imagens\"")
	if not os.path.isdir("imagens/"):
		cria_dir = "mkdir imagens"
		script = open("script.sh", "w")
		script.writelines(cria_dir)
		script.close()
		call(["sh", "script.sh"])
		call(["rm", "script.sh"])
	else:
		print("[!] O diretório já existe.")
		print("[!] Movendo imagens...")
		move_imagens = "mv *.jpg imagens/"
		script = open("script.sh", "w")
		script.writelines(move_imagens)
		script.close()
		call(["sh", "script.sh"])
		call(["rm", "script.sh"])
		print("[+] Ok.")

	print("[+] Pronto.")


def modo_batch(arg):
	imprimir_informacoes()
	testa_conexao()
	links = gerar_links(arg)
	r = baixar_imagens(links)
	for i in r:
		if i != 0:
			print("[-] A imagem referente ao horario requisitado não existe.")
			testa_conexao()
			links = gerar_links(arg)
			r = baixar_imagens(links)
	mover_imagens()


def modo_iterativo():
	print('[*] Modo iterativo')
	imprimir_informacoes()
	n_imagens = input('[?] Número de imagens: ')
	testa_conexao()
	links = gerar_links(n_imagens)
	r = baixar_imagens(links)
	for i in r:
		if i != 0:
			print("[-] A imagem referente ao horario requisitado não existe.")
			d = input("[?] Deseja tentar novamente? [S, n] \n\t> ")
			if d == "S" or d == "s":
				testa_conexao()
				links = gerar_links(arg)
				r = baixar_imagens(links)
			else:
				sys.exit("[!] Ok, saindo...")
	mover_imagens()


def arg_parser(argumentos):
	argumentos.reverse()
	if len(argumentos) == 1:
		modo_iterativo()
	else:
		while len(argumentos) > 0:
			head = argumentos.pop()
			if head == "-n_imagens":
				n_imagens = int(argumentos.pop())
			elif head == "-intervalo":
				global INTERVALO
				INTERVALO = int(argumentos.pop())
			elif head == "-min_inf":
				global MIN_INF
				MIN_INF = int(argumentos.pop())
			elif head == "-min_sup":
				global MIN_SUP
				MIN_SUP = int(argumentos.pop())
			elif head == "-modo":
				global MODO
				MODO = argumentos.pop()
				if MODO != "topo" and MODO != "infravermelho" and MODO != "vapor" and MODO != "visivel":
					print('[-] Erro ao processar os argumentos')
					print('[*] Execute novamente utilizando o parâmetro -ajuda')
					print('    Exemplo: $ ./baixar_goes.py -ajuda')
					sys.exit(0)
			elif head == "-ajuda":
				print_uso_batch()
				sys.exit(0)
			elif head == "-sobre":
				imprimir_informacoes()
				sys.exit(0)

		try:
			modo_batch(n_imagens)
		except:
			print('[-] Erro ao processar os argumentos')
			print('[!] Você deve informar a quantidade de imagens a ser baixada')
			print_uso_batch()


if __name__ == "__main__":
	arg_parser(sys.argv)

