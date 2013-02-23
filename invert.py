#! /usr/bin/python
import sys

# Perform Gaussian elimination to get linear combinations
# to obtain each standard basis vector from given basis vectors.
# We use row operations to convert the input vectors to row-reduced
# eschelon form (if the input vectors span the space this will
# include an identity matrix) and simultaneously perform the same
# row operations on an identity matrix
def invert (vectors):
  def sortkey(x):
    """Reverses the bits in the low-order 32 bytes and negates; this is used
       to put the vectors with lower low-order bits before the vectors with
       higher low-order bits to make sure that we always have pivots."""
    return -sum([1 << (31-i) for i in range(0,32) if x & (1 << i)])
  # adjoin an identity matrix to the left side of our list of vectors
  # after masking off any high-order bits of the vectors to avoid problems
  # if some of the input hashes are negative
  vectors = [(vec & 0xffffffff) | (1 << (32+i)) for i,vec in enumerate(vectors)]
  vectors = sorted(vectors,key=sortkey)
  for i,vec in enumerate(vectors):
    for j in range (i+1,len(vectors)):
      if vectors[j] & lowbit(vectors[i]):
        vectors[j] ^= vectors[i]
    vectors[i+1:len(vectors)] = sorted(vectors[i+1:len(vectors)],key = sortkey)
  vectors = sorted(vectors,key=sortkey)
  for i,vec in reversed(list(enumerate(vectors))):
    for j in range(i-1,-1,-1):
      if vectors[j] & lowbit(vectors[i]):
        vectors[j] ^= vectors[i]
  dontspan = len(vectors) < 32
  for i,vec in enumerate(vectors[0:32]):
    if (vec & 0xffffffff) != (1 << i):
      dontspan = 1
      break
  if dontspan:
    print(vectors)
    print("WARNING: Vectors do not span the space...probably will fail.",file=sys.stderr)
  return vectors

def getRepresentationOfVector(vec,basis):
  result = 0
  for i in range(0,32):
    if vec & (1 << i):
      result ^= basis[i] >> 32
  return result

def bitposns(x):
  l = []
  i = 0
  while x >> i:
    if x & (1 << i):
      l.append(i)
    i += 1
  return l

def printbits (x):
  for i in range(0,32):
    print((x >> (63-i) & 1),end="")
  print(" ",end="")
  for i in range(32,64):
    print((x >> (63-i) & 1),end="")
  print()

def printbasis (l):
  for item in l:
    printbits(item)

def lowbit (x):
  for i in range (0,32):
    y = x & (1 << i)
    if y:
      return y
  return 0

def xorsum (l):
  result = 0
  for i in l:
    result ^= i & 0xFFFFFFFF
  return result

def gethashes (f):
  fh = open(f)
  sonnets = []
  hashes = []
  for line in fh:
    x = line.split()
    sonnets.append(x[2])
    hashes.append(int(x[0]))
  fh.close()
  return sonnets[0], hashes[0], sonnets[1:], [hashes[0] ^ h for h in hashes[1:]]

def getrepresentation (f,goal):
  basesonnet, basehash, sonnets, hashes = gethashes(f)
  basis = invert(hashes)
  x = getRepresentationOfVector(goal^basehash,basis)
  return basehash,hashes,basesonnet,sonnets,bitposns(x)

def getsonnet (f,goal):
  basehash,hashes,basesonnet,sonnets,bps = getrepresentation(f,goal)
  basesonnet = open(basesonnet).read()
  result = list(basesonnet)
  for j in bps:
    s = open(sonnets[j]).read()
    for i, c in enumerate(s):
      if basesonnet[i] != s[i]:
        result[i] = s[i]
  result = ''.join(result)
  print (result,end="")
  return result

if __name__ == '__main__':
  getsonnet(sys.argv[1],int(sys.argv[2]))
