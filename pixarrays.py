from PIL import Image
import numpy as np
from webcolors import rgb_to_name 
import sys,json, piltest,imageSimil,os, shutil
import ast
from datetime import datetime

try:
	fuch = sys.argv[1]
	mosaicSize = int(sys.argv[2])
	numProto = int(sys.argv[3])
	alpha = float(sys.argv[4])
except:
	fuch = 'Pigeon-8.jpg'
	mosaicSize = 2
	numProto = 256
	alpha = 0.01

i = Image.open(fuch).convert('RGB')
iar = np.asarray(i)

print i.mode,i.size
#sys.exit()
img = Image.new(i.mode, i.size)

list_of_pixels = []
list_compressed =[]
mosaic = []

if not os.path.exists('mosaics'):
	os.makedirs('mosaics')

if not os.path.exists('rebuild'):
	os.makedirs('rebuild')

if not os.path.exists('orig'):
	os.makedirs('orig')

folders = ['mosaics','rebuild','orig']
for folder in folders:
	for the_file in os.listdir(folder):
		file_path = os.path.join(folder, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as e:
			print(e)

a = datetime.now()

mosaicDict = piltest.imageCompress(fuch,mosaicSize,numProto,alpha)

imageSimil.codify(fuch,mosaicDict,mosaicSize)

b= datetime.now()
print 'Original size = ' + str(os.path.getsize(fuch))
print 'compress time',str(b-a)

filr = open('decipheredText','r').read()
#print filr
newDict = ast.literal_eval(filr)

a = datetime.now()
imageSimil.rebuild(fuch,newDict,mosaicSize,numProto)
b = datetime.now()
print 'decompress time',str(b-a)
print 'Original size = ' + str(os.path.getsize('cipheredText'))