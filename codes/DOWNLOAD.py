from subprocess import *
from glob import glob
#coding: utf-8

def download(url):
	httpsPort = str(url.replace("\n",":443"))
	resultado = str(url.replace("\n",".pem"))

	comandoCriarArquivo = ['touch', resultado]

	processoCriarArquivo = Popen(comandoCriarArquivo, stdout=PIPE)
	[response, error] = processoCriarArquivo.communicate()
	processoCriarArquivo.wait()
	
	certificado = open(resultado, 'w')

	comando_a = ['openssl', 's_client', '-showcerts', '-connect', httpsPort] 
	comando_b = ['openssl', 'x509', '-outform', 'PEM']
	#openssl s_client -showcerts -connect matriculaweb.unb.br:443 | openssl x509 -outform PEM > mycert.pem
	
	process_a = Popen(comando_a, stdout=PIPE)
	process_b = Popen(comando_b, stdin=process_a.stdout, stdout=certificado)
	[response, error] = process_b.communicate()
	process_b.wait()

	certificado.close()
	pass
	
if __name__ == '__main__':
	with open('links.lnk') as f:
		listaDeLinks = f.readlines()

	f.close()

	for link in listaDeLinks:
		download(link)