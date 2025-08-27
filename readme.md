# Summary

SixtyFourdleMinimumSolution.py accepts a list of words which compose the solution to the game at https://64ordle.au/

The goal of the program is to identify the smallest possible number words that need to be solved in order to trigger the auto complete. 

This was coded mostly by Gemini initially but I found their PyCharm plugin trying so I switched at some point to Claude.

# Execution Time

The core words are calculated instantly so the general time to run is most governed by the size of the solutions minus the size of the core word set. In other words, how many additional words are needed beyond the core words for a minimal solution. 
This dictates how many times we must run the loop. The speed of the loop is moderately affected by the number of dominated words. The more dominated words, the fewer combinations we need to check.

See an example run for an example execution time for a relatively long run. 

# How it works

The program first starts by identifying any words that must be in every solution set by searching for all words which have a letter in a position that no other word has. 

It then constructs a representation of the problem space, which contains a list of all distinct letter/position combinations.

We apply our common words directly on that solution set and identify any remaining letter/position combinations.

Next we check for "dominated words", which are words whose contributions to the solution would be a strict subset of the contributions of another word meaning it will never appear in our minimal solution so we exclude it from our search space.

After removing the "dominated words" we check again for additional common words which further reduces our search space. 

Then we take the set of words that aren't in our common set, and search each subset of size 1 to see if it solves. If not, we get a list of all distinct subsets of size 2 and so on. The larger the size of the subset, the more distinct subsets exist which is what primarily governs the speed of execution. 

At the end we print a list of all possible solution sets and presents them broken down into the following: 

- The core words found before starting the analysis.

- The words beyond the core words which exist in every minimal solution

- Groupings of solution sets with multiple common words and separating the suffix's for easier exploration of the solution space. 

# My process

We initially started with an utterly naive/brute force process. 

That proceeded slowly so I looked at a few ways of speeding things up. 

My first approach revolved around sorting all the letters by numbers of occurrences and searched for the minimum groups of words required to cover those letters for the least common to most common. I would let the program stop when it no longer had non unique solutions. 

I would proceed this way until I reached a set of letters with multiple solutions. This was not a good approach as there were instances in which a set of three letters had multiple solutions, but a set of 5 didn't. In addition this search itself was exceedingly slow. 

The big break through was not looking for letters by number of instances but simply looking for words which had a distinct letter/position combination. That meant these words HAD to be in the solution set and thus so were all the additional letters in that word reducing the size of the solution space by several orders of magnitude.

The script ran fine on smaller solution spaces (ones where we had a lot of core words), but was still too slow if the puzzle solution was large enough. 

After some prodding, Gemini suggested looking for words in the remaining search space (non-core words) whose contributions are a strict subset of another word. Since using the "dominated" word would never be optimal, we remove that word from the search space, providing another magnitudinal jump in performance.

From there after a few iterations, I've settled on grouping solution sets based on common elements as an easier way to read the solution space.

Later we added dominated words, and then looking at it's attempts to solve certain problems, found that we would benefit from checking again after the dominated words. 

# Sample

## Answers from 2025-08-27

AWOKE ~ KHAKI ~ UPSET ~ SMILE ~ PRISM ~ FLANK ~ FIXED ~ ELIDE		WRUNG ~ MOLLY ~ BELLE ~ RASPY ~ CUTIE ~ CRANK ~ WHELP ~ LINGO
ABEAM ~ BOGUS ~ SWUNG ~ PLANK ~ QUIRK ~ SHARP ~ WIDEN ~ BLOAT		WAKED ~ MERIT ~ GREET ~ POSER ~ RAINY ~ WENCH ~ DJINN ~ DINGE
~	
BOGEY ~ UNFIT ~ IMPEL ~ KNEAD ~ WOODY ~ CHILL ~ CURRY ~ AGORA		CAIRN ~ PAYER ~ RESIN ~ FLUTE ~ SINCE ~ BEGAT ~ GROAN ~ QUEER
CELLO ~ GAFFE ~ BEACH ~ DUMPY ~ INANE ~ HAVEN ~ CHEST ~ LOTUS		GEESE ~ DRAPE ~ GRAND ~ LOFTY ~ GORED ~ REHAB ~ CLING ~ LAPSE

## Output

Starting analysis for a list of 64 words.

--------------------------------------------------

Found 17 unique letter-positions that must be covered by mandatory words.

Found 14 mandatory words based on unique positions: ['ABEAM', 'AGORA', 'DJINN', 'DUMPY', 'ELIDE', 'FIXED', 'GAFFE', 'HAVEN', 'KHAKI', 'PAYER', 'REHAB', 'UPSET', 'WAKED', 'WIDEN']

--------------------------------------------------

Searching for all minimal solutions...

Optimization: Pruned 18 dominated words from the search space.

Dominated words will not ever appear in a minimum solution set.

Dominated words: ['AWOKE', 'BEGAT', 'BLOAT', 'BOGEY', 'CAIRN', 'DINGE', 'DRAPE', 'FLANK', 'GEESE', 'GRAND', 'GREET', 'GROAN', 'KNEAD', 'PLANK', 'POSER', 'QUEER', 'RESIN', 'WOODY']

Found 4 additional core words after pruning: ['BOGUS', 'LINGO', 'QUIRK', 'SWUNG']

Checking for solutions of size 19 (took 0.00s)

Checking for solutions of size 20 (took 0.00s)

Checking for solutions of size 21 (took 0.00s)

Checking for solutions of size 22 (took 0.02s)

Checking for solutions of size 23 (took 0.14s)

Checking for solutions of size 24 (took 0.51s)

Checking for solutions of size 25 (took 1.63s)

Checking for solutions of size 26 (took 4.05s)

Checking for solutions of size 27 (took 8.77s)

Found 104 minimal solution(s) of size 27.

--------------------------------------------------

An ideal solution contains the following (20 words):

  Core words: ['ABEAM', 'AGORA', 'DJINN', 'DUMPY', 'ELIDE', 'FIXED', 'GAFFE', 'HAVEN', 'KHAKI', 'PAYER', 'REHAB', 'UPSET', 'WAKED', 'WIDEN']

  Additional common words: ['BOGUS', 'IMPEL', 'LINGO', 'PRISM', 'QUIRK', 'SWUNG']

--------------------------------------------------

Select all elements in the first set and one of the second sets (second sets are usually single words)

  ['BEACH', 'CELLO', 'INANE', 'LOTUS', 'MERIT', 'SHARP'] -- [['FLUTE'], ['LOFTY']]

  ['BEACH', 'CELLO', 'INANE', 'LOTUS', 'MERIT', 'WHELP'] -- [['FLUTE'], ['LOFTY']]

  ... Omitted for brevity

  ['CUTIE', 'LOFTY', 'MOLLY', 'UNFIT', 'WENCH', 'WHELP'] -- [['CURRY'], ['GORED']]

  ['CUTIE', 'MERIT', 'MOLLY', 'SHARP', 'UNFIT', 'WENCH'] -- [['FLUTE'], ['LOFTY']]

  ['CUTIE', 'MERIT', 'MOLLY', 'UNFIT', 'WENCH', 'WHELP'] -- [['FLUTE'], ['LOFTY']]
