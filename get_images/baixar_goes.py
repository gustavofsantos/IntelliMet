#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Autor: Gustavo Fernandes dos Santos
# Email: gfdsantos@inf.ufpel.edu.br
# versão 1.01

# Área de carregamento de módulos
from datetime import datetime
from subprocess import call
from calendar import monthrange
import os
import sys
import urllib.request as request

class BaixadorGOES:
	GOES_topo          = "http://www.inmet.gov.br/projetos/cga/capre/sepra/GEO/GOES12/AMERICA_SUL/AS12_TN"
	GOES_visivel       = "http://www.inmet.gov.br/projetos/cga/capre/sepra/GEO/GOES12/AMERICA_SUL/AS12_VI"
	GOES_infravermelho = "http://www.inmet.gov.br/projetos/cga/capre/sepra/GEO/GOES12/AMERICA_SUL/AS12_IV"
	GOES_vapor         = "http://www.inmet.gov.br/projetos/cga/capre/sepra/GEO/GOES12/AMERICA_SUL/AS12_VA"

	GOES_BRASIL_visivel = "http://www.inmet.gov.br/projetos/sepis/GOES12/REGIOES/BRASIL/br_VI"
	GOES_BRASIL_infravermelho = "http://www.inmet.gov.br/projetos/sepis/GOES12/REGIOES/BRASIL/br_IV"
	GOES_BRASIL_vapor = "http://www.inmet.gov.br/projetos/sepis/GOES12/REGIOES/BRASIL/br_VA"
	GOES_BRASIL_vapor_realc = "http://www.inmet.gov.br/projetos/sepis/GOES12/REGIOES/BRASIL/br_VPR"
	GOES_BRASIL_topo = "http://www.inmet.gov.br/projetos/sepis/GOES12/REGIOES/BRASIL/br_TN"

	SE_RECUPEROU       = False
	TRANSF15PARA14 	   = False
	INTERVALO          = 30
	MIN_SUP            = 30
	MIN_INF            = 0
	MODO               = "topo"
	REGIAO			   = "brasil"

	LISTA_MINUTOS      = []

	def __init__(self):
		self.identidade = 0

	@classmethod
	def imprimir_informacoes(self):
		"""
		Imprime as informaçoes do desenvolvedor
		"""
		#call(["clear"])
		print("    -----------------INFORMAÇÕES-----------------")
		print("[*] Baixador de imagens do INMET. v0.95")
		print("[*] Autor: Gustavo Fernandes dos Santos")
		print("[*] Email: gfdsantos@inf.ufpel.edu.br")
		print("    -----------------------------------")
		print("[!] Imagens são produto do GOES - América Latina")
		print("    * Topo das núvens")
		print("    * Visível")
		print("    * Infravermelho termal")
		print("    * Vapor d'Agua")
		print("    -----------------------------------")
		print("[*] Usando intervalo de {} minutos".format(BaixadorGOES.INTERVALO))
		print("[*] Usando a banda de {}".format(BaixadorGOES.MODO))
		print("    -----------------INFORMAÇÕES-----------------")


	@classmethod
	def print_uso_batch(self):
		print("""[*] Modo de uso em batch:
	    $ ./baixar_goes.py <lista de argumentos>
		ou
		$ python baixar_goes.py <lista de argumentos>

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


	
	@classmethod
	def print_erro(self):
		print("[-] Erro na inicializaçao.")
		print("[!] Execute novamente utilizando como argumento \"ajuda\".")
		print("[!] Exemplo: $ ./get_imagens.py ajuda")


	@classmethod
	def testa_conexao(self):
		print("[!] Estabelecendo conexao...")
		try:
			url_open = request.urlopen("http://www.inmet.gov.br")
			if url_open.getcode() != 200:
				sys.exit("[-] Sem conexão.")
		except:
			sys.exit("[-] Sem conexão.")

		


	@classmethod
	def imagem_online(self, link):
		print("[!] Testando o link:")
		print("    " + link)

		try:
			url_open = request.urlopen(link)
			if url_open.getcode() == 200:
				print("[+] Imagen online.")
				return True
			else:
				print("[-] Imagem offline.")
				return False
		except:
			print("[-] Imagem offline.")
			return False


	def retrocede2(self, ano, mes, dia, hora, minuto):
		minuto = minuto - self.INTERVALO
		if minuto < 0:
			minuto = 60 - self.INTERVALO
			hora = hora - 1
			if hora < 0:
				hora = 23
				dia = dia - 1
				if dia <= 0:
					mes = mes - 1
					if mes <= 0:
						mes = 12
						ano = ano - 1
					dia = monthrange(ano, mes)



	@classmethod
	def retrocede(self, ano, mes, dia, hora, minuto):
		if minuto == 14:
			minuto = 15
		minuto = minuto - self.INTERVALO
		if minuto == 15:
			if self.TRANSF15PARA14:
				minuto = 14
		if minuto < 0:
			minuto = 60 - self.INTERVALO
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
			
			if self.MIN_SUP < 60:
				minuto = self.MIN_SUP
			else:
				minuto = 0
		else:
			minuto = self.MIN_INF
		return (ano, mes, dia, hora, minuto)


	@classmethod
	def gerar_links(self, arg):
		print('[*] Gerando {} links para imagens do GOES'.format(arg))

		hora = datetime.now().hour
		minuto = datetime.now().minute
		dia = datetime.now().day
		mes = datetime.now().month
		ano = datetime.now().year

		if minuto > 0: minuto = self.INTERVALO
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

		if self.REGIAO == "america_sul":
			if self.MODO == "topo":
				preLink = self.GOES_topo
			elif self.MODO == "visivel":
				preLink = self.GOES_visivel
			elif self.MODO == "infravermelho":
				preLink = self.GOES_infravermelho
			elif self.MODO == "vapor":
				preLink = self.GOES_vapor

		if self.REGIAO == "brasil":
			if self.MODO == "topo":
				preLink = self.GOES_BRASIL_topo
			elif self.MODO == "visivel":
				preLink = self.GOES_BRASIL_visivel
			elif self.MODO == "infravermelho":
				preLink = self.GOES_BRASIL_infravermelho
			elif self.MODO == "vapor":
				preLink = self.GOES_BRASIL_vapor
			elif self.MODO == "vapor_realc":
				preLink = self.GOES_BRASIL_vapor_realc

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
			ano, mes, dia, hora, minuto = BaixadorGOES.retrocede(ano, mes, dia, hora, minuto)

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

			if BaixadorGOES.imagem_online(link):
				links.append(link)
				e = 0
			else:
				i = i - 1
				e = e + 1
				if e >= 10: 
					print('[-] Foi identificado falha ao testar se as 10 ultimas imagens estão online.')
					print('[*] Verifique a sua conexão com a internet')
					print('[*] Verifique se o INMET está online')
					print('[*] Verifique se os links gerados condizem com os disponíveis no site.')
					if not self.SE_RECUPEROU:
						print('[!] Tentando se recuperar...')
						if self.INTERVALO != 15:
							BaixadorGOES.INTERVALO = 15
						elif self.INTERVALO != 30:
							BaixadorGOES.INTERVALO = 30
						else:
							self.INTERVALO = 60
						e = 0
					else:
						sys.exit("[!] Saindo...")

			i = i + 1

		return links


	@classmethod
	def baixar_imagens(self, links):
		print("[+] Baixando imagens...\n")

		r = []
		for link in links:
			imagem_nome = link.split('/')[-1]
			uopen = request.urlopen(link)
			if uopen.getcode() != 200:
				r.append(uopen.getcode())
			else:
				meta = uopen.getheaders()
				tamanho = int(meta[5][1])
				print("[!] Baixando {} de {} bytes".format(imagem_nome, tamanho))
				with uopen as resp, open(imagem_nome, 'wb') as imagem_saida:
					dados = resp.read()
					imagem_saida.write(dados)
				
				r.append(uopen.getcode())

		return r


	@classmethod
	def mover_imagens(self):
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


	@classmethod
	def modo_batch(self, arg):
		BaixadorGOES.imprimir_informacoes()
		BaixadorGOES.testa_conexao()
		links = BaixadorGOES.gerar_links(arg)
		r = BaixadorGOES.baixar_imagens(links)
		for i in r:
			if i != 200:
				print("[-] A imagem referente ao horario requisitado não existe.")
				BaixadorGOES.testa_conexao()
				links = BaixadorGOES.gerar_links(arg)
				r = BaixadorGOES.baixar_imagens(links)
		#BaixadorGOES.mover_imagens()


	@classmethod
	def modo_iterativo(self):
		print('[*] Modo iterativo')
		BaixadorGOES.imprimir_informacoes()
		n_imagens = input('[?] Número de imagens: ')
		BaixadorGOES.testa_conexao()
		links = BaixadorGOES.gerar_links(n_imagens)
		r = BaixadorGOES.baixar_imagens(links)
		for i in r:
			if i != 0:
				print("[-] A imagem referente ao horario requisitado não existe.")
				d = input("[?] Deseja tentar novamente? [S, n] \n\t> ")
				if d == "S" or d == "s":
					BaixadorGOES.testa_conexao()
					links = BaixadorGOES.gerar_links(arg)
					r = BaixadorGOES.baixar_imagens(links)
				else:
					sys.exit("[!] Ok, saindo...")
		BaixadorGOES.mover_imagens()


	def arg_parser(self, argumentos):
		argumentos.reverse()
		n_imagens = 0
		if len(argumentos) == 1:
			BaixadorGOES.modo_iterativo()
		else:
			while len(argumentos) > 0:
				head = argumentos.pop()
				if head == "--nimagens":
					n_imagens = int(argumentos.pop())
				elif head == "--intervalo":
					BaixadorGOES.INTERVALO = int(argumentos.pop())
					BaixadorGOES.MIN_SUP = 60 - BaixadorGOES.INTERVALO
				elif head == "--min_inf":
					BaixadorGOES.MIN_INF = int(argumentos.pop())
				elif head == "--min_sup":
					BaixadorGOES.MIN_SUP = int(argumentos.pop())
				elif head == "--regiao": # brasil ou america_sul
					BaixadorGOES.REGIAO = argumentos.pop()
					if self.REGIAO != "brasil" and self.REGIAO != "america_sul":
						print('[-] Erro ao processar os argumentos')
						print('[*] Execute novamente utilizando o parâmetro -ajuda')
						print('    Exemplo: $ ./baixar_goes.py -ajuda')
						sys.exit(0)
				elif head == "--modo":
					BaixadorGOES.MODO = argumentos.pop()
					if self.MODO != "topo" and self.MODO != "infravermelho" and self.MODO != "vapor" and self.MODO != "visivel":
						print('[-] Erro ao processar os argumentos')
						print('[*] Execute novamente utilizando o parâmetro -ajuda')
						print('    Exemplo: $ ./baixar_goes.py -ajuda')
						sys.exit(0)
				elif head == "--bug":
					BaixadorGOES.TRANSF15PARA14 = True
				elif head == "-ajuda":
					BaixadorGOES.print_uso_batch()
					sys.exit(0)
				elif head == "-sobre":
					BaixadorGOES.imprimir_informacoes()
					sys.exit(0)

			if n_imagens > 0:
				BaixadorGOES.modo_batch(n_imagens)
			else:
				print('[-] Erro ao processar os argumentos')
				print('[!] Você deve informar a quantidade de imagens a ser baixada')
				BaixadorGOES.print_uso_batch()



if __name__ == "__main__":
	bg = BaixadorGOES();
	bg.arg_parser(sys.argv)

