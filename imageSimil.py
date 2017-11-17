from itertools import izip
from PIL import Image
import sys
from os import listdir
from os.path import isfile, join
import numpy as np
from PIL import ImageChops
import math, operator
import imagehash
import run

def eval(i1name,i2name):

	#i2name = i2name.replace('mosaics/','')

	print i1name,i2name,'meeee'

	if i2name == i1name:
		return 0

	i1 = Image.open(i1name)
	i2 = Image.open(i2name)
	#assert i1.mode == i2.mode, "Different kinds of images."
	#assert i1.size == i2.size, "Different sizes."
	 
	pairs = izip(i1.getdata(), i2.getdata())
	if len(i1.getbands()) == 1:
	    # for gray-scale jpegs
	    dif = sum(abs(p1-p2) for p1,p2 in pairs)
	else:
	    dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))

	ncomponents = i1.size[0] * i1.size[1] * 3
	return (dif / 255.0 * 100) / ncomponents

def matrixEval(air1,air2):

	res1 = []
	res2 = []

	for asd in range(0,len(air1)-1):
		for ad in range(0,len(air1[asd])-1):
			#ou o avg dos 3 valores
			res1.append(air1[asd][ad][0])
			res1.append(air1[asd][ad][1])
			res1.append(air1[asd][ad][2])

			res2.append(air2[asd][ad][0])
			res2.append(air2[asd][ad][1])
			res2.append(air2[asd][ad][2])

	return abs(sum(res1)-sum(res2))

def realDist(air1,air2):
	#print np.linalg.norm(air1-air2)
	return np.sqrt(np.sum((air1-air2)**2))

def realDist2(air1,air2):
	#print np.linalg.norm(air1-air2)
	return np.sum(air1-air2)

def matrixEval2(air1,air2):

	res1 = []
	res2 = []

	for asd in range(0,len(air1)-1):
		for ad in range(0,len(air1[asd])-1):
			#ou o avg dos 3 valores
			res1.append(air1[asd][ad][0])
			res1.append(air1[asd][ad][1])
			res1.append(air1[asd][ad][2])

			res2.append(air2[asd][ad][0])
			res2.append(air2[asd][ad][1])
			res2.append(air2[asd][ad][2])

	return sum(res1)-sum(res2)

def codify(imgName,mosaicDict,mosaicSize):

	res1 = []

	img = Image.open(imgName)
	(imageWidth, imageHeight)=img.size

	name = imgName.split('.')[0]

	gridx=mosaicSize
	gridy=gridx
	rangex=imageWidth/gridx
	rangey=imageHeight/gridy
	finalList = {}
	finalToLZW = [[],[]]
	freqs = {}


	print rangex*rangey,rangex,rangey

	finalImage = Image.new('RGB',(imageWidth,imageHeight))

	integer = 0

	print 'Building codex'

	for x in xrange(rangex):
		#print x/(rangex*100)," percent complete         \r",
		for y in xrange(rangey):
			bbox=(x*gridx, y*gridy, x*gridx+gridx, y*gridy+gridy)
			slice_bit=img.crop(bbox)
			savix = 'rebuild/'+name+'_xmap_'+str(x)+'_'+str(y)+'.jpg'
			slice_bit.save(savix)
			#print savix,'savix'

			i = Image.open(savix)
			iar = np.asarray(i)

			chosenMosaic = {'name':'','grade':-1,'struct':[]}

			for mosaicName,mosaicAir in mosaicDict.items():
				iar2 = np.asarray(mosaicAir)

				diff_a_b = realDist(iar2,iar)

				if chosenMosaic['grade'] == -1:
					chosenMosaic['grade'] = diff_a_b
					chosenMosaic['name'] = mosaicName
					chosenMosaic['struct'] = mosaicAir
				elif chosenMosaic['grade'] > diff_a_b:
					chosenMosaic['grade'] = diff_a_b
					chosenMosaic['name'] = mosaicName
					chosenMosaic['struct'] = mosaicAir

			if chosenMosaic['name'] not in finalToLZW[0]:
				finalToLZW[0].append(chosenMosaic['name'])
				finalToLZW[1].append(finalToLZW[0].index(chosenMosaic['name']))
			else:
				finalToLZW[1].append(finalToLZW[0].index(chosenMosaic['name']))

			finalImage.paste(Image.open(chosenMosaic['name']), bbox)

	#finalImage.show()
	#print 'Running LZW',finalToLZW
	run.runnit(finalToLZW)

def rebuild(imgName,newDict,mosaicSize,numProto):

	res1 = []

	img = Image.open(imgName)
	(imageWidth, imageHeight)=img.size

	name = imgName.split('.')[0]

	gridx=mosaicSize
	gridy=gridx
	rangex=imageWidth/gridx
	rangey=imageHeight/gridy
	finalList = {}
	finalToLZW = []

	#print rangex*rangey,rangex,rangey

	finalImage = Image.new('RGB',(imageWidth,imageHeight))

	integer = 0

	for x in xrange(rangex):
		#print x/(rangex*100)," percent complete         \r",
		for y in xrange(rangey):
			bbox=(x*gridx, y*gridy, x*gridx+gridx, y*gridy+gridy)
			slice_bit=img.crop(bbox)
			savix = 'rebuild/'+name+'_xmap_'+str(x)+'_'+str(y)+'.jpg'
			slice_bit.save(savix)
			#print savix,'savix'

			i = Image.open(savix)
			iar = np.asarray(i)

			chosenMosaic = {'name':'','grade':-1}

			entry = newDict[0][newDict[1][integer]]

			finalImage.paste(Image.open(entry), bbox)
			integer += 1

	finalImage.save('final' + str(mosaicSize) +'_' +str(numProto) + '.jpg')
	finalImage.show()

def rmsdiff(im1, im2):
	"Calculate the root-mean-square difference between two images"
	diff = ImageChops.difference(im1, im2)
	h = diff.histogram()
	sq = (value*(idx**2) for idx, value in enumerate(h))
	sum_of_squares = sum(sq)
	rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
	return rms

def hashingdiff(im1,im2):
	ahash = imagehash.average_hash(im1)
	otherhash = imagehash.average_hash(im2)
	return int(ahash - otherhash)



