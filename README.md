Bloom Filter

A Python implementation of a Bloom filter: a probabilistic data structure that tests whether an item is in a set. It allows a tunable rate of false positives but never gives a false negative. It uses a bit array and multiple hash functions to map items, so lookups are fast and memory-efficient, and the actual data is never stored.

How It Works
Adding an item: the item is run through several hash functions. Each hash picks a position in the bit array, and those bits are set to 1.
Checking an item: the item is hashed the same way. If any of its bits is 0, the item is definitely not in the set. If all of its bits are 1, the item is probably in the set.

This is why false negatives are impossible, but false positives can happen: different items can happen to set the same bits. The false positive rate is set by the size of the bit array and the number of hash functions.

Project Structure
Requirements
Python 3.14 or newer
Packages in the files folder
How to Run
Clone the repository: git clone https://github.com/ChanaRapp/bloom-filter.git
Move into the folder: cd bloom-filter
Run the program: python BloomFilter.py
Example Usage
Written in main() at the bottom of BloomFilter.py, using /data/wordlist.txt

Test Data

data/wordlist.txt is a list of words used to test the filter. Some of the words are added to the filter, and then another group of the words not in the list is checked to measure the false positive rate.

Credits
BitHash.py:
__author__  = "Avinash Kak (kak@purdue.edu)"
__date__    = '2021-May-30'
__url__     = 'https://engineering.purdue.edu/kak/dist/BitVector-3.5.0.html'
__copyright__ = "(C) 2021 Avinash Kak. Python Software Foundation."
BitVector.py and wordlist.txt: from my professor

What I Learned

Building this showed me how a Bloom filter trades a small, controllable chance of error for large savings in memory and speed. 
Using several hash functions on one bit array keeps both insertion and lookup at O(k), where k is the number of hash functions. 
Since k is fixed, that is effectively constant time no matter how many items are stored. Because bits are only ever set, never cleared, 
a lookup can never miss an item that was added, so there are no false negatives. The only error is a false positive, when other items 
have happened to set all the same bits. That rate can be calculated from the size of the bit array, the number of hash functions, 
and the number of items inserted, so I could choose those parameters to hit a target rate. 
With 100000 words and four hash functions, my measured false positive rate was 5.003%, close to the predicted 5.0079%
