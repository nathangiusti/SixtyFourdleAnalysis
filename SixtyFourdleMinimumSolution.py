import itertools
from collections import Counter, defaultdict


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

    candidate_words = [w for w in unique_words if
                       w not in core_combo and not remaining_universe.isdisjoint(word_coverage_map[w])]

    min_k_extra = float('inf')
    for k_extra in range(1, len(candidate_words) + 1):
        if k_extra > min_k_extra:
            break
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
            # --- Analysis of Swappable Word Pairs ---
            all_non_common_words = set.union(*(s - common_words for s in all_solutions))
            candidate_pairs = itertools.combinations(sorted(list(all_non_common_words)), 2)

            swappable_pairs = []
            non_common_sets = [s - common_words for s in all_solutions]

            for pair in candidate_pairs:
                w1, w2 = pair
                is_swappable = True
                # Check if exactly one of the pair is in each non-common set (XOR)
                for non_common_set in non_common_sets:
                    if (w1 in non_common_set) == (w2 in non_common_set):
                        is_swappable = False
                        break
                if is_swappable:
                    swappable_pairs.append(sorted(pair))

            if swappable_pairs:
                print("Take one from each of the following groups")
                for pair in sorted(swappable_pairs):
                    print(f"  - {pair}")

            print("-" * 50)

            # --- Distinct solution sets minus common and paired words ---
            all_paired_words = {word for pair in swappable_pairs for word in pair}
            distinct_residual_sets = set()
            for s in all_solutions:
                residual_set = frozenset(s - common_words - all_paired_words)
                distinct_residual_sets.add(residual_set)

            if not any(distinct_residual_sets):
                print("  (All non-common words are part of swappable pairs)")
            else:
                sorted_residuals = sorted([sorted(list(s)) for s in distinct_residual_sets])
                # Group sets by their common n-1 prefix
                groups = defaultdict(list)
                single_sets = []
                for res_set in sorted_residuals:
                    n = len(res_set)
                    if n >= 2:  # A set needs at least 2 elements to have a prefix and a suffix for grouping
                        prefix = tuple(res_set[:-1])
                        suffix = res_set[-1]  # The last element
                        groups[prefix].append(suffix)
                    else:
                        # Sets with 0 or 1 elements cannot be grouped by prefix
                        single_sets.append(res_set)

                # Identify true groups (more than one member) and move singletons
                final_groups = {}
                for prefix, suffixes in groups.items():
                    if len(suffixes) > 1:
                        # The suffixes are single words, so we just sort them
                        final_groups[prefix] = sorted(suffixes)
                    else:
                        # This was not a group, so reconstruct the original set and add to singles
                        single_sets.append(list(prefix) + suffixes)

                # Print grouped sets
                if final_groups:
                    print("Take the common prefix and one of the following endings:")
                    for prefix, suffixes in sorted(final_groups.items()):
                        print(f"  - Common: {list(prefix)}, Endings: {suffixes}")
                # Print remaining individual sets
                if single_sets:
                    print("Or one of these sets")
                    for s in sorted(single_sets):
                        print(f"  - {s}")
            print("-" * 50)

        full_universe = set().union(*word_coverage_map.values())
        covered_by_common = set().union(*(word_coverage_map[w] for w in sorted_common_words))
        uncovered_by_common = full_universe - covered_by_common