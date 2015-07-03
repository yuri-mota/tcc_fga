from subprocess import *
from glob import glob

def download_root(certificado):
	comando_um = ['openssl', 'x509', '-in', certificado, '-text']
	
	process = Popen(comando_um, stdout=PIPE)
	[response, error] = process.communicate()
	process.wait()

	tokens = response.split()
	
	foundIssuers = False
	foundScore = False
	
	download_link = ""
	
	#procura o link do CA Issuers e joga em download_link
	for token in tokens:
		if foundIssuers and foundScore:
			download_link = str(token)
			foundIssuers = False
		if token == 'Issuers':
			foundIssuers = True
			foundScore = False
		if token == '-':
			foundScore = True
			
	##tirando os primeiros quatro caracteres "URI:" e impurezas
	download_link = download_link[4:]
	#download_link = download_link.split(":")[-1]
	#download_link = 'http:' + download_link
	print download_link
	
	#nome do arquivo baixado
	nome_download = download_link.split("/")[-1]
	print nome_download
	
	comando_dois = ['wget', download_link]
	
	process = Popen(comando_dois, stdout=PIPE)
	[response, error] = process.communicate()
	process.wait()
	
	#determinando o nome final do arquivo
	na_root = str(certificado.replace(".crt", ""))
	na_root = na_root + '.root'
	print na_root
	
	#comando para passar de DER para PEM
	comando_tres = ['openssl', 'x509', '-in', nome_download, '-inform', 'der', '-out', na_root, '-outform', 'pem']
	
	process = Popen(comando_tres, stdout=PIPE)
	[response, error] = process.communicate()
	process.wait()
	
	#comando para deletar o DER original
	comando_quatro = ['rm', '-r', nome_download]
	
	process = Popen(comando_quatro, stdout=PIPE)
	[response, error] = process.communicate()
	process.wait()
	
	
	
if __name__ == '__main__':

	files = glob("*.crt")
	
	for certificado in files:
		download_root(certificado)
