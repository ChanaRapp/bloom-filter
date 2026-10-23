# Bloom Filter

A Python implementation of a Bloom filter: a probabilistic data structure that tests whether an item is in a set. It allows a tunable rate of false positives but never gives a false negative. It uses a bit array and multiple hash functions to map items, so lookups are fast and memory-efficient, and the actual data is never stored.

## How It Works

- **Adding an item:** The item is run through several hash functions. Each hash picks a position in the bit array, and those bits are set to `1`.
- **Checking an item:** The item is hashed the same way.
  - If **any** of its bits is `0`, the item is **definitely not** in the set.
  - If **all** of its bits are `1`, the item is **probably** in the set.

This is why false negatives are impossible but false positives can happen: different items can happen to set the same bits. The false positive rate is determined by the size of the bit array, the number of hash functions, and the number of items inserted.

## Project Structure

```
bloom-filter/
├── BloomFilter.py      # Bloom filter implementation and example run
├── BitHash.py          # Hash function helper
├── BitVector.py        # Bit array implementation
└── wordlist.txt        # Word list used for testing
```

## Requirements

- Python 3.14 or newer
- The supporting modules (`BitHash.py`, `BitVector.py`) are included in the repository

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/ChanaRapp/bloom-filter.git
   ```
2. Move into the folder:
   ```bash
   cd bloom-filter
   ```
3. Run the program:
   ```bash
   python BloomFilter.py
   ```

## Usage

### API

```python
from BloomFilter import BloomFilter

# Sized for 100,000 keys, 4 hash functions, and a 5% target false positive rate
bf = BloomFilter(numKeys=100000, numHashes=4, maxFalsePositive=0.05)

bf.insert("apple")
bf.find("apple")    # True  -> "apple" MAY be in the filter
bf.find("banana")   # False -> "banana" is definitely not in the filter
```

| Method | Description |
|---|---|
| `BloomFilter(numKeys, numHashes, maxFalsePositive)` | Creates a filter and calculates the number of bits needed to hit the target false positive rate |
| `insert(key)` | Adds a key to the filter |
| `find(key)` | Returns `True` if the key *may* have been inserted, `False` if it definitely was not |
| `falsePositiveRate()` | Returns the projected false positive rate based on the number of bits actually set |
| `numBitsSet()` | Returns the number of bits currently set |

### Example Run

Running `BloomFilter.py` executes `__main()`, which:

1. Inserts the first 100,000 words from `wordlist.txt`.
2. Prints the projected false positive rate, based on the bits actually set.
3. Re-reads those same words and counts any that are missing, which should always be `0`.
4. Checks the next 100,000 words, none of which were inserted, and counts how many are falsely found.
5. Prints the measured false positive rate.

## Test Data

`wordlist.txt` is a list of words used to test the filter. The first 100,000 words are added to the filter, and the next 100,000 words, which were never added, are checked to measure the false positive rate. The file must contain at least 200,000 words.

## Results

With 100,000 words and four hash functions:

| Measured false positive rate | Predicted false positive rate |
|:----------------------------:|:-----------------------------:|
| 5.003%                       | 5.0079%                       |

## What I Learned

Building this showed me how a Bloom filter trades a small, controllable chance of error for large savings in memory and speed.

- **Constant-time operations:** Using several hash functions on one bit array keeps both insertion and lookup at O(k), where k is the number of hash functions. Since k is fixed, that is effectively constant time no matter how many items are stored.
- **No false negatives:** Bits are only ever set, never cleared, so a lookup can never miss an item that was added.
- **Predictable false positives:** The only error is a false positive, when other items have happened to set all the same bits. That rate can be calculated from the size of the bit array, the number of hash functions, and the number of items inserted, so I could choose those parameters to hit a target rate.
- **Theory matched practice:** My measured false positive rate of 5.003% was very close to the predicted 5.0079%.

## Credits

- **`BitHash.py`**
  - Author: Avinash Kak (kak@purdue.edu)
  - Date: 2021-May-30
  - Source: [BitVector 3.5.0](https://engineering.purdue.edu/kak/dist/BitVector-3.5.0.html)
  - Copyright (C) 2021 Avinash Kak. Python Software Foundation.
- **`BitVector.py`** and **`wordlist.txt`**: provided by my professor
