from PIL import Image
import numpy as np
import imageSimil,sys,random,os
from os import listdir
from os.path import isfile, join
from collections import Counter

global allPrototypes
global distList
global allMosaics

allPrototypes = {}
distList = {}
allMosaics = {}

def createPrototypes(fuch,mosaicSize,numProto):

	img = Image.open(fuch)
	(imageWidth, imageHeight)=img.size

	name = fuch.split('.')[0]
	print name

	gridx=mosaicSize
	gridy=gridx
	rangex=imageWidth/gridx
	rangey=imageHeight/gridy

	print rangex*rangey,rangex,rangey

	fileList = 'mosaics'
	fileList = [f for f in listdir(fileList) if isfile(join(fileList, f))  and ('.jpg' in f or '.png' in f) and name in f]
	selectedList = random.sample(range(0, (rangex*rangey)-1), numProto)

	k = 0

	for x in xrange(rangex):
		#print x/(rangex*100)," percent complete         \r",
		for y in xrange(rangey):
			bbox=(x*gridx, y*gridy, x*gridx+gridx, y*gridy+gridy)
			slice_bit=img.crop(bbox)

			#save originals for future comparison
			savixOrig = 'orig/'+name+'_xmap_'+str(x)+'_'+str(y)+'.jpg'
			slice_bit.save(savixOrig)

			i = Image.open(savixOrig)
			iar = np.asarray(i)

			allMosaics[savixOrig] = iar

			if k in selectedList:
				savix = 'mosaics/'+name+'_xmap_'+str(x)+'_'+str(y)+'.jpg'
				slice_bit.save(savix)
				allPrototypes[savix] = iar

			k+=1
	print

def imageCompress(myFile, mosaicSize, numProto,alpha):

	res = {}

	print 'Creating prototypes'
	createPrototypes(myFile,mosaicSize, numProto)
	i = -1

	print 'Training prototypes'
	#train prototypes

	for i in range(1):

		for aname1, air1 in allMosaics.items():
			i += 1

			#print i/len(allMosaics.keys())*100," percent complete         \r",

			winner = {'name':'','grade':-1}

			i1 = Image.open(aname1)
			a = np.asarray(air1)

			for aname2, air2 in allPrototypes.items():

				b = np.asarray(air2)

				dist_a_b = imageSimil.realDist(b,a)
				#print dist_a_b

				if winner['grade'] == -1:
					winner['name'] = aname2
					winner['grade'] = dist_a_b
				elif winner['grade'] > dist_a_b:
					winner['name'] = aname2
					winner['grade'] = dist_a_b

			#difference = a.astype(np.int16) - allPrototypes[winner['name']].astype(np.int16)
			difference = allPrototypes[winner['name']].astype(np.int16) - a.astype(np.int16)

			#ver alpha e int(alpha * np.sum(difference)) o difference .astype('uint8') .astype(np.int16)
			mult = np.multiply(difference,alpha)
			#print mult[0],'mult'
			before = allPrototypes[winner['name']][0]
			allPrototypes[winner['name']] = np.add(allPrototypes[winner['name']].astype(np.int16),mult.astype(np.int16))
			#print np.absolute(allPrototypes[winner['name']][0]),'abs'
			after = allPrototypes[winner['name']][0]
			#print after - before
			im = Image.fromarray(np.absolute(allPrototypes[winner['name']]).astype('uint8'))
			im.save(winner['name'])


	return allPrototypes

def dist(x,y):   
    return np.sqrt(np.sum((x-y)**2))