# Summary

SixtyFourdleMinimumSolution.py accepts a list of words which compose the solution to the game at https://64ordle.au/

The goal of the program is to identify the smallest possible number of words that need to be solved in order to trigger the auto complete. 

This was coded mostly by Gemini initially but I found their PyCharm plugin trying, so I switched at some point to Claude.

# Execution Time

The core words are calculated instantly, so the general time to run is mostly governed by the size of the solutions minus the size of the core word set. In other words, how many additional words are needed beyond the core words for a minimal solution. 
This dictates how many times we must run the loop. The speed of the loop is moderately affected by the number of dominated words. The more dominated words, the fewer combinations we need to check.

See an example run for an example execution time for a relatively long run. 

# How it works

The program first starts by identifying any words that must be in every solution set by searching for all words which have a letter in a position that no other word has. 

It then constructs a representation of the problem space, which contains a list of all distinct letter/position combinations.

We apply our core words directly to that solution set and identify any remaining letter/position combinations.

Next we check for "dominated words", which are words whose contributions to the solution would be a strict subset of the contributions of another word, meaning it will never appear in our minimal solution, so we exclude it from our search space.

We continue this process until we no longer find additional core or dominated words.  

Then we take the set of words that aren't in our core set, and search each subset of size 1 to see if it solves. If not, we get a list of all distinct subsets of size 2 and so on. The larger the size of the subset, the more distinct subsets exist, which is what primarily governs the speed of execution. 

At the end we print a list of all possible solution sets and present them broken down into the following: 

- The core words found before starting the analysis.

- The words beyond the core words which exist in every minimal solution

- Groupings of solution sets with multiple common words and separating the suffixes for easier exploration of the solution space. 

# My process

We initially started with an utterly naive/brute force process. 

That proceeded slowly so I looked at a few ways of speeding things up. 

My first approach revolved around sorting all the letters by number of occurrences and searching for the minimum groups of words required to cover those letters from the least common to most common. I would let the program stop when it no longer had non-unique solutions. 

I would proceed this way until I reached a set of letters with multiple solutions. This was not a good approach as there were instances in which a set of three letters had multiple solutions, but a set of 5 didn't. In addition, this search itself was exceedingly slow. 

The big breakthrough was not looking for letters by number of instances but simply looking for words which had a distinct letter/position combination. That meant these words HAD to be in the solution set and thus so were all the additional letters in that word, reducing the size of the solution space by several orders of magnitude.

The script ran fine on smaller solution spaces (ones where we had a lot of core words), but was still too slow if the puzzle solution was large enough. 

After some prodding, Gemini suggested looking for words in the remaining search space (non-core words) whose contributions are a strict subset of another word. Since using the "dominated" word would never be optimal, we remove that word from the search space, providing another order-of-magnitude jump in performance.

From there after a few iterations, I've settled on grouping solution sets based on common elements as an easier way to read the solution space.

Later we added dominated words, and then looking at its attempts to solve certain problems, found that we would benefit from checking again after removing the dominated words.

After an especially long run, I realized we should just continue that process iteratively until we no longer find new words. 

# Sample

## Answers from 2025-08-27

AWOKE ~ KHAKI ~ UPSET ~ SMILE ~ PRISM ~ FLANK ~ FIXED ~ ELIDE		WRUNG ~ MOLLY ~ BELLE ~ RASPY ~ CUTIE ~ CRANK ~ WHELP ~ LINGO
ABEAM ~ BOGUS ~ SWUNG ~ PLANK ~ QUIRK ~ SHARP ~ WIDEN ~ BLOAT		WAKED ~ MERIT ~ GREET ~ POSER ~ RAINY ~ WENCH ~ DJINN ~ DINGE
~	
BOGEY ~ UNFIT ~ IMPEL ~ KNEAD ~ WOODY ~ CHILL ~ CURRY ~ AGORA		CAIRN ~ PAYER ~ RESIN ~ FLUTE ~ SINCE ~ BEGAT ~ GROAN ~ QUEER
CELLO ~ GAFFE ~ BEACH ~ DUMPY ~ INANE ~ HAVEN ~ CHEST ~ LOTUS		GEESE ~ DRAPE ~ GRAND ~ LOFTY ~ GORED ~ REHAB ~ CLING ~ LAPSE

## Output

```
Starting analysis for a list of 64 words.
--------------------------------------------------
Found 19 unique letter-positions that must be covered by mandatory words.
Found 16 mandatory words based on unique positions: ['ADDER', 'AGENT', 'ANKLE', 'APHID', 'ASSAY', 'AXIOM', 'CRUEL', 'DRIFT', 'EVADE', 'FABLE', 'FICUS', 'MACAW', 'MELON', 'METER', 'NEIGH', 'SCUBA']
--------------------------------------------------
Searching for all minimal solutions...
Iteration 1: Starting with 46 candidate words
Iteration 1: Pruned 14 dominated words: ['AEGIS', 'ALIAS', 'APNEA', 'ARMED', 'CRIMP', 'DOULA', 'DRESS', 'ERECT', 'INANE', 'LEAKY', 'SAVOY', 'SCONE', 'SHANK', 'SMELT']
Iteration 1: Found 2 additional core words: ['CHAMP', 'INGOT']
Iteration 2: Starting with 30 candidate words
Iteration 2: Pruned 2 dominated words: ['GRIME', 'SHAKY']
Iteration 3: Starting with 28 candidate words
Iteration 3: No more dominated words or core words found. Stopping iterative process.
Checking for solutions of size 19 (took 0.00s)
Checking for solutions of size 20 (took 0.00s)
Checking for solutions of size 21 (took 0.01s)
Checking for solutions of size 22 (took 0.04s)
Checking for solutions of size 23 (took 0.23s)
Checking for solutions of size 24 (took 0.90s)
Checking for solutions of size 25 (took 2.99s)
Checking for solutions of size 26 (took 8.23s)
Checking for solutions of size 27 (took 19.56s)
Checking for solutions of size 28 (took 39.88s)
Found 1 minimal solution(s) of size 28.
--------------------------------------------------
An ideal solution contains the following (28 words):
  Core words (unique position analysis): ['ADDER', 'AGENT', 'ANKLE', 'APHID', 'ASSAY', 'AXIOM', 'CHAMP', 'CRUEL', 'DRIFT', 'EVADE', 'FABLE', 'FICUS', 'INGOT', 'MACAW', 'MELON', 'METER', 'NEIGH', 'SCUBA']
  Additional core words (common to all solutions): ['BLESS', 'CHORE', 'EMPTY', 'GRAVY', 'LIVER', 'PINKY', 'RASPY', 'THICK', 'WORDY', 'YUMMY']
--------------------------------------------------
```
