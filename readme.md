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

The script ran fine on smaller solution spaces (ones where we had a lot of core words), but was still too slow if the puzzle solution was large enough. 

After some prodding, Gemini suggested looking for words in the remaining search space (non-core words) whose contributions are a strict subset of another word. Since using the "dominated" word would never be optimal, we remove that word from the search space, providing another magnitudinal jump in performance.

From there after a few iterations, I've settled on grouping solution sets based on common elements as an easier way to read the solution space.

# Sample

## Input list from 2025-08-13

"IGLOO", "SWATH", "CORAL", "NAKED", "BOTCH", "EDIFY", "CORGI", "TONAL",	"WHICH", "DOGMA", "SLIME", "WREAK", "JELLY", "BULKY", "LOVED", "FILED", "AGAIN", "SHAME", "GLAND", "OUTGO", "SAINT", "SQUID", "GLEAM", "SHRUG",	"EXUDE", "ACORN", "AIMER", "FEWER", "BEGUN", "ADOPT", "RUMBA", "FULLY",	"CINCH", "WAVER", "SINEW", "VERSE", "TUBER", "GAZER", "OBESE", "PAYER",	"EVADE", "SAMBA", "IRONY", "BLITZ", "CHUMP", "SWEPT", "MAYOR", "BLASE", "GIZMO", "SHOOT", "LINER", "PAPAL", "BOWED", "SLACK", "SCALP", "SPERM",	"SHONE", "SMILE", "BINGE", "MERRY", "SLASH", "OVINE", "SOLAR", "ROUND"

## Output

Starting analysis for a list of 64 words.
--------------------------------------------------
Found 18 unique letter-positions that must be covered by mandatory words.
Found 17 mandatory words based on unique positions: ['BLITZ', 'BULKY', 'CORGI', 'DOGMA', 'EDIFY', 'EXUDE', 'JELLY', 'NAKED', 'OBESE', 'PAPAL', 'SHRUG', 'SINEW', 'SMILE', 'SPERM', 'SQUID', 'TUBER', 'VERSE']
--------------------------------------------------
Searching for all minimal solutions...
Optimization: Pruned 16 dominated words from the search space.
Checking for solutions of size 18
Checking for solutions of size 19
Checking for solutions of size 20
Checking for solutions of size 21
Checking for solutions of size 22
Checking for solutions of size 23
Checking for solutions of size 24
Checking for solutions of size 25
Checking for solutions of size 26
Checking for solutions of size 27
Checking for solutions of size 28
Checking for solutions of size 29
Found 3 minimal solution(s) of size 29.
--------------------------------------------------
An ideal solution contains the following (26 words):
  ['BLITZ', 'BOTCH', 'BULKY', 'CORGI', 'DOGMA', 'EDIFY', 'EXUDE', 'FEWER', 'GIZMO', 'JELLY', 'LOVED', 'MAYOR', 'NAKED', 'OBESE', 'PAPAL', 'RUMBA', 'SCALP', 'SHRUG', 'SINEW', 'SMILE', 'SPERM', 'SQUID', 'SWEPT', 'TUBER', 'VERSE', 'WREAK']
--------------------------------------------------
Select all elements in the first set and one in the second set
  ['AGAIN', 'IRONY'] -- [['EVADE'], ['OVINE']]
Or one of these set(s)
  - ['ACORN', 'IGLOO', 'OVINE']
--------------------------------------------------