from BitHash import *
from BitVector import *

class BloomFilter(object):
    '''
    Return the estimated number of bits needed in a Bloom Filter 
    that will store numKeys keys, using numHashes hash functions, 
    and that will have a false positive rate of maxFalsePositive.
    '''
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        phi = 1-(maxFalsePositive**(1/numHashes))
        return numHashes / (1-(phi**(1/numKeys)))
    
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        '''
        Create a Bloom Filter that will store numKeys keys, using
        numHashes hash functions, and that will have a false positive 
        rate of maxFalsePositive.
        '''
        self.__bits = int(self.__bitsNeeded(numKeys, numHashes, maxFalsePositive) + .5)   
        self.__BitVector = BitVector(intVal=0, size=self.__bits)
        self.__numKeys = numKeys
        self.__numHashes = numHashes
        self.__maxFalsePositive = maxFalsePositive
        self.__nItems = 0
    
    def insert(self, key):
        ''' Insert the specified key into the Bloom Filter '''
        for i in range(1, self.__numHashes+1):
            if self.__BitVector[BitHash(key, hashFuncNum=i) % self.__bits] == 0: self.__nItems += 1
            self.__BitVector[BitHash(key, hashFuncNum=i) % self.__bits] = 1 
    
    def find(self, key):
        ''' Returns True if key MAY have been inserted into the Bloom filter. 
        Returns False if key definitely hasn't been inserted into the BF. '''
        for i in range(1, self.__numHashes+1):
            if self.__BitVector[BitHash(key, hashFuncNum=i) % self.__bits] == 0:
                return False
        return True  
    
    def falsePositiveRate(self):
        '''
        Returns the PROJECTED current false positive rate based on the
        ACTUAL current number of bits actually set in this Bloom Filter. 
        '''
        d = self.__numHashes
        phi = (self.__bits - self.numBitsSet()) / self.__bits     
        return (1-phi)**d
       
    def numBitsSet(self):
        ''' Returns the current number of bits ACTUALLY set in this Bloom Filter '''
        return self.__nItems
       
def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
    
    # create the Bloom Filter
    BF = BloomFilter(numKeys, numHashes, maxFalse)
    # read the first numKeys words from the file and insert them 
    # into the Bloom Filter. Close the input file.
    words = open("wordlist.txt")
    for i in range(numKeys):
        BF.insert(words.readline())
    words.close()
    # Print out what the PROJECTED false positive rate should 
    # THEORETICALLY be based on the number of bits that ACTUALLY ended up being set
    # in the Bloom Filter. 
    print(f'False positive rate should be: {BF.falsePositiveRate()}')
    # Re-open the file, and re-read the same bunch of the first numKeys 
    # words from the file and count how many are missing from the Bloom Filter, 
    # printing out how many are missing. 
    words = open("wordlist.txt")
    count = 0
    for i in range(numKeys):
        if BF.find(words.readline()) == False: count += 1
    print(f'Missing: {count}')
    # Read the next numKeys words from the file, none of which 
    # have been inserted into the Bloom Filter, and count how many of the 
    # words can be (falsely) found in the Bloom Filter.
    falsePositives = 0
    for i in range(numKeys):
        if BF.find(words.readline()) == True: falsePositives += 1
    words.close()    
    print(f'False Positives: {falsePositives}')    
    # Print out the percentage rate of false positives.
    print(f'False positive percentage rate: {falsePositives/numKeys} = {(falsePositives/numKeys * 100)}%')
    
if __name__ == '__main__':
    __main()       