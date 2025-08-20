import itertools
from collections import Counter
import re
import time


#


ANSWERS = """
 COPY AND PASTE THE ANSWER BLOB FROM THE WEBSITE HERE. THE CODE WILL EXTRACT THE WORDS
"""
# EX:
# ANSWERS = """
# LYRIC ~ BOUND ~ BRASH ~ SURGE ~ AXION ~ DINGO ~ CHOSE ~ SNIDE		AUNTY ~ HALVE ~ WRECK ~ SWEPT ~ DISHY ~ FOCAL ~ RIDER ~ REACH
# EXULT ~ LEARN ~ TRAIN ~ CURRY ~ UPSET ~ DOTED ~ TWIST ~ PLUNK		GLAND ~ BULLY ~ COBRA ~ WAVER ~ NEVER ~ LEMUR ~ FINED ~ FUMED
# ~
# REVUE ~ REBUT ~ ULTRA ~ CHUNK ~ GIZMO ~ SIZED ~ VYING ~ CRAVE		SCRAP ~ STUNG ~ FOLIO ~ NOSEY ~ DRIFT ~ BLOND ~ LINGO ~ GAUDY
# DUTCH ~ PRISM ~ LURED ~ ENTRY ~ FLUNG ~ GLOAT ~ LIKED ~ TOWED		COYLY ~ CRUEL ~ FIELD ~ RANCH ~ HAUNT ~ DUMMY ~ CLUEY ~ BONEY
# """


def find_mandatory_words_for_unique_positions(words: list[str]) -> list[str]:
	"""
	Identifies a core set of words that are mandatory because they cover
	a (letter, position) pair that appears in no other word.
	"""
	if not words:
		return []
	unique_words = sorted(list(set(words)))
	position_counts = Counter((letter, i) for word in unique_words for i, letter in enumerate(word))
	unique_positions = {pos for pos, count in position_counts.items() if count == 1}

	if not unique_positions:
		print("No unique letter-positions found. The mandatory core is empty.")
		return []

	print(f"Found {len(unique_positions)} unique letter-positions that must be covered by mandatory words.")

	core_combo = set()
	for word in unique_words:
		for i, letter in enumerate(word):
			if (letter, i) in unique_positions:
				core_combo.add(word)
				break
	return sorted(list(core_combo))


def find_solutions_from_core_generator(words: list[str], core_combo: list[str], word_coverage_map):
	"""
	A generator that finds and yields all minimal solutions given a pre-defined core.
	"""
	unique_words = sorted(list(set(words)))
	full_universe = set().union(*word_coverage_map.values())

	if not full_universe:
		return

	covered_by_core = set().union(*(word_coverage_map[w] for w in core_combo if w in word_coverage_map))
	remaining_universe = full_universe - covered_by_core

	if not remaining_universe:
		yield sorted(core_combo)
		return

	# Step 1: Initial filtering of candidate words.
	# Only consider words not in the core that cover something in the remaining universe.
	initial_candidates = [w for w in unique_words if
						  w not in core_combo and not remaining_universe.isdisjoint(word_coverage_map[w])]

	# Step 2: Prune dominated words to reduce the search space.
	# A word is dominated if its contribution to the remaining universe is a
	# strict subset of another candidate's contribution. Using such a word is never optimal.
	candidate_contributions = {w: word_coverage_map[w] & remaining_universe for w in initial_candidates}

	dominated_words = set()
	items = list(candidate_contributions.items())
	for w1, c1 in items:
		if w1 in dominated_words:
			continue
		for w2, c2 in items:
			if w1 == w2:
				continue
			# If w2's contribution is a proper subset of w1's, w2 is dominated.
			if c2 < c1:
				dominated_words.add(w2)

	candidate_words = [w for w in initial_candidates if w not in dominated_words]

	if dominated_words:
		print(f"Optimization: Pruned {len(dominated_words)} dominated words from the search space.")
		print("Dominated words will not ever appear in a minimum solution set.")
		print(f"Dominated words: {sorted(list(dominated_words))}")

	min_k_extra = float('inf')
	for k_extra in range(1, len(candidate_words) + 1):
		start_time = time.time()
		if k_extra > min_k_extra:
			break
		print(f"Checking for solutions of size {k_extra + len(core_combo)}", end="")

		# Precompute maximum possible coverage for pruning
		# all_remaining_coverage = set().union(*(word_coverage_map[w] & remaining_universe for w in candidate_words))

		for i, extra_words_tuple in enumerate(itertools.combinations(candidate_words, k_extra)):
			# Early termination: check if remaining words can cover what's still needed
			if i % 1000 == 0 and i > 0:  # Check periodically to avoid overhead
				covered_so_far = set().union(*(word_coverage_map[w] for w in extra_words_tuple))
				still_needed = remaining_universe - covered_so_far

				if still_needed:
					# Get remaining candidate words not yet in this combination
					used_words = set(extra_words_tuple)
					remaining_words = [w for w in candidate_words if w not in used_words]
					remaining_coverage = set().union(
						*(word_coverage_map[w] & still_needed for w in remaining_words)) if remaining_words else set()

					# If remaining words cannot cover what's still needed, skip this branch
					if not still_needed.issubset(remaining_coverage):
						continue

			covered_by_extra = set().union(*(word_coverage_map[w] for w in extra_words_tuple))
			if remaining_universe.issubset(covered_by_extra):
				min_k_extra = k_extra
				yield sorted(core_combo + list(extra_words_tuple))
		
		elapsed_time = time.time() - start_time
		print(f" (took {elapsed_time:.2f}s)")


# --- Main Execution Workflow ---
if __name__ == '__main__':
	word_list_1 = re.findall(r'\b[A-Z]{5}\b', ANSWERS)

	print(f"Starting analysis for a list of {len(word_list_1)} words.")
	print("-" * 50)

	unique_words = sorted(list(set(word_list_1)))
	word_coverage_map = {word: set((letter, i) for i, letter in enumerate(word)) for word in unique_words}

	mandatory_core = find_mandatory_words_for_unique_positions(word_list_1)
	if mandatory_core:
		print(f"Found {len(mandatory_core)} mandatory words based on unique positions: {mandatory_core}")
	print("-" * 50)

	print(f"Searching for all minimal solutions...")
	all_solutions = [set(s) for s in find_solutions_from_core_generator(word_list_1, mandatory_core, word_coverage_map)]

	if not all_solutions:
		print("Could not find any solution to cover all letters.")
	else:
		print(f"Found {len(all_solutions)} minimal solution(s) of size {len(all_solutions[0])}.")
		print("-" * 50)

		common_words = set.intersection(*all_solutions)
		sorted_common_words = sorted(list(common_words))
		core_words = [word for word in sorted_common_words if word in mandatory_core]
		additional_common_words = [word for word in sorted_common_words if word not in mandatory_core]
		print(f"An ideal solution contains the following ({len(sorted_common_words)} words):")
		print(f"  Core words: {core_words}")
		print(f"  Additional common words: {additional_common_words}")
		print("-" * 50)

		if len(all_solutions) > 1:
			# --- Analysis of Distinct Non-Common Sets ---
			distinct_residual_sets = set()
			for s in all_solutions:
				# A residual set is what's left of a solution after removing the common core.
				residual_set = frozenset(s - common_words)
				distinct_residual_sets.add(residual_set)

			if not any(distinct_residual_sets):
				# This case is unlikely if solutions differ, but included for completeness.
				print("  (No non-common words found across solutions)")
			else:
				# Iteratively find the largest common subsets among the residual sets.
				sets_to_process = list(distinct_residual_sets)
				final_groups = []

				while len(sets_to_process) > 1:
					# Find all non-empty subsets of each set and count their occurrences.
					subset_counts = Counter()
					for s in sets_to_process:
						s_list = sorted(list(s))
						for k in range(1, len(s_list) + 1):
							for subset in itertools.combinations(s_list, k):
								subset_counts[subset] += 1

					# Find subsets that appear in at least two sets.
					common_subsets = {subset: count for subset, count in subset_counts.items() if count >= 2}

					if not common_subsets:
						break  # No more groups can be formed.

					# Find the largest common subset to form the next group.
					best_common_subset = max(common_subsets, key=lambda k: (len(k), k))
					best_common_frozenset = frozenset(best_common_subset)

					# Collect all sets that contain this common subset and separate them.
					group_members = [s for s in sets_to_process if best_common_frozenset.issubset(s)]
					sets_to_process = [s for s in sets_to_process if not best_common_frozenset.issubset(s)]

					# Store the found group for printing.
					other_words = [sorted(list(s - best_common_frozenset)) for s in group_members]
					final_groups.append((sorted(list(best_common_frozenset)), sorted(other_words)))

				# Print grouped sets
				if final_groups:
					print(
						"Select all elements in the first set and one of the second sets (second sets are usually single words)")
					for common, others in sorted(final_groups):
						print(f"  {common} -- {others}")
				# Print remaining individual sets
				if sets_to_process:
					if final_groups:
						print("Or one of these set(s)")
					else:
						print("One of these set(s)")
					for s in sorted([sorted(list(s)) for s in sets_to_process]):
						print(f"  - {s}")
			print("-" * 50)

		full_universe = set().union(*word_coverage_map.values())
		covered_by_common = set().union(*(word_coverage_map[w] for w in sorted_common_words))
		uncovered_by_common = full_universe - covered_by_common