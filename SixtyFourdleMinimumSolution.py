import itertools
from collections import Counter


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

    min_k_extra = float('inf')
    for k_extra in range(1, len(candidate_words) + 1):
        if k_extra > min_k_extra:
            break
        print(f"Checking for solutions of size {k_extra + len(core_combo)}")
        for extra_words_tuple in itertools.combinations(candidate_words, k_extra):
            covered_by_extra = set().union(*(word_coverage_map[w] for w in extra_words_tuple))
            if remaining_universe.issubset(covered_by_extra):
                min_k_extra = k_extra
                yield sorted(core_combo + list(extra_words_tuple))


# --- Main Execution Workflow ---
if __name__ == '__main__':
    word_list_1 = []

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
        print(f"An ideal solution contains the following ({len(sorted_common_words)} words):\n  {sorted_common_words}")
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
                    print("Select all elements in the first set and one in the second set")
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