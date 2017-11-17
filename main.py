import huffman

input = "aababcabcd"

print huffman(input)

print len(input) * 8, len(huffman(input)[1])

input = "the quick brown fox jumps over the lazy dog" 
print huffman(input)

print len(input) * 8, len(huffman(input)[1])

import urllib
input = urllib.urlopen("http://docs.python.org/lib/front.html").read()

print len(input) * 8, len(huffman(input)[1])

input = file("wrnpc12.txt").read()
print len(input) * 8, len(huffman(input)[1])