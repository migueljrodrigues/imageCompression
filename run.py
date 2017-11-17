import huffman,lzw,os
from datetime import datetime
from bitarray import bitarray
from guppy import hpy
import numpy as np

def lzwhuffRun(txt):

	a = datetime.now()
	codebook = huffman.makeFrequencies(txt)
	cipher = ''.join(codebook[c] for c in txt)
	cipher = lzw.lzwCode(cipher)
	b = datetime.now()

	#plotterAlgs.cipherTime.append((b-a))
	#print "cipherTime: " + str((b-a).microseconds)

	f = open('cipheredText', 'wb')
	a = bitarray(cipher)
	f.write(a)
	f.close()

	#print 'Ciphered size = ' + str(os.path.getsize('cipheredText'))
	#plotterAlgs.cipherSize.append(os.path.getsize('cipheredText'))

	a = datetime.now()
	decipher = lzw.lzwDecode(cipher)
	decipher = huffman.decode(decipher, codebook)
	b = datetime.now()

	#plotterAlgs.decipherTime.append(b-a)
	#print "decipherTime: " + str((b-a).microseconds)

	f2 = open('decipheredText', 'w')
	f2.write(str(decipher))
	f2.close()

	#printar = open('decipheredText','r')
	#print #printar.read()[:40]
	#printar.close()

	#print 'Back to original = ' + str(os.path.getsize('decipheredText'))
	#plotterAlgs.decipherSize.append(os.path.getsize('decipheredText'))

def runnit(recv):
	txt = str(recv)
	#print 'Original size = ' + str(sys.getsizeof(recv))#str(os.path.getsize('bible-kjv.txt'))
	#print 

	print 'LZW + Huffman'
	a = datetime.now()
	lzwhuffRun(txt)
	b= datetime.now()
	print str(b-a)
	print