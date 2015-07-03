from subprocess import *
from glob import glob

def erros():
	erros = {0 : 'ok',
		1 : 'ok',
		2 : 'unable to get issuer certificate',
		3 : 'unable to get certificate CRL',
		4 : 'unable to decrypt certificate\'s signature',
		5 : 'unable to decrypt CRL\'s signature',
		6 : 'unable to decode issuer public key',
		7 : 'certificate signature failure',
		8 : 'CRL signature failure',
		9 : 'certificate is not yet valid',
		10 : 'certificate has expired',
		11 : 'CRL is not yet valid',
		12 : 'CRL has expired',
		13 : 'format error in certificate\'s notBefore field',
		14 : 'format error in certificate\'s notAfter field',
		15 : 'format error in CRL\'s lastUpdate field',
		16 : 'format error in CRL\'s nextUpdate field',
		17 : 'out of memory',
		18 : 'self signed certificate',
		19 : 'self signed certificate in certificate chain',
		20 : 'unable to get local issuer certificate',
		21 : 'unable to verify the first certificate',
		22 : 'certificate chain too long',
		23 : 'certificate revoked',
		24 : 'invalid CA certificate',
		25 : 'path length constraint exceeded',
		26 : 'unsupported certificate purpose',
		27 : 'certificate not trusted',
		28 : 'certificate rejected',
		29 : 'subject issuer mismatch',
		30 : 'authority and subject key identifier mismatch',
		31 : 'authority and issuer serial number mismatch',
		32 : 'key usage does not include certificate signing',
		50 : 'application verification failure'}
	return erros

def find_subject(certificado):
	comando_um = ['openssl', 'x509', '-in', certificado, '-text']
	
	process = Popen(comando_um, stdout=PIPE)
	[response, error] = process.communicate()
	process.wait()

	tokens = response.split('O=')
	
	token = ""
	token = tokens[2]
	micro = token.split(',')
	subject = micro[0]
	sub = subject.split('/')
	return str(sub[0])

def find_issuer(certificado):
	comando_um = ['openssl', 'x509', '-in', certificado, '-text']
	
	process = Popen(comando_um, stdout=PIPE)
	[response, error] = process.communicate()
	process.wait()

	tokens = response.split('O=')
	
	token = ""
	token = tokens[1]
	micro = token.split(',')
	issuer = micro[0]
	iss = issuer.split('/')
	return str(iss[0])

def separador_c():
	certificados = []
	c = ""
	arquivo = open('lista.dupla','r')
	for line in arquivo:
		c = str(line.split(',')[0])
		certificados.append(str(c))
	return certificados
	
def separador_r():
	roots = []
	r = ""
	arquivo = open('lista.dupla','r')
	for line in arquivo:
		r = str(line.split(',')[1])
		roots.append(str(r.replace("\n","")))
	return roots
	
def verifica_c(certificado):
	args = ['openssl', 'verify', certificado]

	process = Popen(args, stdout=PIPE)
	[response, error] = process.communicate()
	process.wait()

	tokens = response.split()

	issuer = find_issuer(certificado)
	company = '-'

	foundError = False
	errorCode = 1

	for token in tokens:
		if foundError:
			errorCode = int(token)
			foundError = False	

		if token == 'error':
			foundError = True
	
	error_list = erros()
	
	message = ""
	message = error_list[int(errorCode)]
	
	dados = (errorCode, message, certificado, issuer)

	return dados
	
def verifica_rc(certificado, root):
	args = ['openssl', 'verify', '-CAfile', root, certificado]

	process = Popen(args, stdout=PIPE)
	[response, error] = process.communicate()
	process.wait()

	issuer = find_issuer(certificado)
	company = '-'
	
	tokens = response.split()

	foundError = False
	errorCode = 1

	for token in tokens:
		if foundError:
			errorCode = int(token)
			foundError = False	

		if token == 'error':
			foundError = True
	
	error_list = erros()
	
	message = ""
	message = error_list[int(errorCode)]
	
	if errorCode == 1:
		errorCode = 0
	
	dados = (errorCode, message, certificado, issuer)
	
	return dados
	
if __name__ == '__main__':
	certificado = separador_c()
	root = separador_r()
	
	for c, r in zip(certificado, root):
		if (r == "-"):
			dados = verifica_c(c)
			print '%d,%s,%s,%s' % dados
		else:
			dados = verifica_rc(c, r)
			print '%d,%s,%s,%s' % dados
	
