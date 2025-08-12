# Summary

SixtyFourdleMinimumSolution.py accepts a list of words which compose the solution to the game at https://64ordle.au/

The goal of the program is to identify the smallest possible number words that need to be solved in order to trigger the auto complete. 

This was coded mostly by Gemini with my guidance. 

# How it works

The program first starts by identifying any words that must be in every solution set by searching for all words which have a letter in a position that no other word has. 

It then constructs a representation of the problem space, which contains a list of all distinct letter/position combinations.

We apply our common words directly on that solution set and identify any remaining letter/position combinations.

Then we take the set of words that aren't in our common set, and search each subset of size 1 to see if it solves. If not, we get a list of all distinct sets of size 2 and so on. 

Our code generates a list of all possible solution sets and presents them broken down into the following. 

First any words that appear in every minimum length solution. 

Then any pairs of words of which, each minimum solution contains exactly one. 

And then looks for any simple groupings of the remaining solution words. 

# My process

We initially started with an utterly naive/brute force process. 

That proceeded slowly so I looked at a few ways of speeding things up. 

My first approach revolved around sorting all the letters by numbers of occurrences and searched for the minimum groups of words required to cover those letters for the least common to most common. I would let the program stop when it no longer had non unique solutions. 

I would proceed this way until I reached a set of letters with multiple solutions. This was not a good approach as there were instances in which a set of three letters had multiple solutions, but a set of 5 didn't. In addition this search itself was exceedingly slow. 

The big break through was not looking for letters by number of instances but simply looking for words which had a distinct letter/position combination. That meant these words HAD to be in the solution set and thus so were all the additional letters in that word reducing the size of the solution space by several orders of magnitude. 

This approach has the program running near instantly on my desktop computer. 

From there I thought of different ways to break out the input (looking for interchangeable pairs of words and the final groupings) to make it easy to understand the space of the solution sets.

# Sample

## Input list from 2025-08-12

"WEARY", "IDYLL", "BRINK", "GORGE", "BALER", "FULLY", "YIELD", "WRIST", "SNACK", "BLAST", "INFRA",
"PLIED", "BIDDY", "HEDGE", "PILED", "HOVER", "SOWED", "JADED", "OLDER", "SCORN", "PROWL", "DRILL",
"BLEEP", "EQUIP", "ARRAY", "WENCH", "GRUNT", "REBUS", "AISLE", "RESIN", "CILIA", "SNOOP", "POUND",
"GIDDY", "SONAR", "FINED", "BRUNT", "EYING", "LINER", "TROLL", "DAGGY", "NUDGE", "SLOSH", "TOWED",
"WRONG", "RAPID", "TUILE", "TRYST", "VIGOR", "SLAKE", "AMISS", "BAWDY", "FLOOD", "BREAD", "FURRY",
"BALMY", "BRUSH", "SPREE", "FATTY", "MYRRH", "ALONE", "PROXY", "BROOM", "TIGHT"

## Output

Starting analysis for a list of 64 words.

--------------------------------------------------

Found 26 unique letter-positions that must be covered by mandatory words.

Found 24 mandatory words based on unique positions: 

['AMISS', 'BALMY', 'BROOM', 'CILIA', 'EQUIP', 'FATTY', 'HOVER', 'IDYLL', 'INFRA', 'JADED', 'LINER', 'MYRRH', 'NUDGE', 'OLDER', 'PROWL', 'PROXY', 'RAPID', 'REBUS', 'SCORN', 'SLAKE', 'SPREE', 'TIGHT', 'VIGOR', 'YIELD']

--------------------------------------------------
Searching for all minimal solutions...

Found 60 minimal solution(s) of size 31.

--------------------------------------------------

An ideal solution contains the following (26 words):

['AMISS', 'BALMY', 'BROOM', 'CILIA', 'EQUIP', 'FATTY', 'HOVER', 'IDYLL', 'INFRA', 'JADED', 'LINER', 'MYRRH', 'NUDGE', 'OLDER', 'PROWL', 'PROXY', 'RAPID', 'REBUS', 'SCORN', 'SLAKE', 'SNACK', 'SPREE', 'TIGHT', 'VIGOR', 'WRONG', 'YIELD']

--------------------------------------------------

Take one from each of the following groups
  - ['AISLE', 'RESIN']
  - ['DAGGY', 'DRILL']

--------------------------------------------------

Take the common prefix and one of the following endings:
  - Common: ['ARRAY', 'BAWDY'], Endings: ['GIDDY', 'GORGE', 'GRUNT']
  - Common: ['ARRAY', 'GIDDY'], Endings: ['SOWED', 'TOWED']
  - Common: ['BAWDY', 'BREAD'], Endings: ['GIDDY', 'GORGE', 'GRUNT']
  - Common: ['BREAD', 'GIDDY'], Endings: ['SOWED', 'TOWED']
  - Common: ['GIDDY', 'SONAR'], Endings: ['SOWED', 'TOWED']

Or one of these sets
  - ['BAWDY', 'GIDDY', 'SONAR']
  - ['BAWDY', 'GORGE', 'SONAR']
  - ['BAWDY', 'GRUNT', 'SONAR']

--------------------------------------------------



