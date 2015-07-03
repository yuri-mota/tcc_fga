from subprocess import *
from glob import glob
# coding: utf-8

def listar():
	file = open('lista.dupla', 'w')
	
	temp_a = ""
	temp_b = ""
	output = ""
	
	CRT = glob("*.crt")
	ROOT = glob("*.root")
	
	match = False
	
	for temp_a in CRT:
		temp_a = str(temp_a.replace(".crt",""))
		match = False
		for temp_b in ROOT:
			temp_b = str(temp_b.replace(".root",""))
			if (temp_a == temp_b) and (match == False):
				dados = (temp_a +'.crt',temp_b + '.root')
				output = '%s,%s\n'%dados
				match = True
			if (match == False):
				dados = (temp_a +'.crt')
				output = '%s,-\n'%dados
				
		if match == True:
			file.write(output)
		else:
			file.write(output)
	
	file.close()
	
if __name__ == '__main__':

	listar()
