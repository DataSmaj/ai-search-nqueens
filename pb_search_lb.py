import random
import time

from n_queens import make_random_board
from n_queens import get_conflicts
from n_queens import get_all_neighbors


#pick the best k boards from a list
#pick the best k boards from a list
#lower conflicts is better
def keep_best_k(board_list, k):

    scored = []

    #score each board one time
    for b in board_list:
        s = get_conflicts(b)
        scored.append((s, b))

    #sort by the score
    scored.sort(key=lambda x: x[0])

    #pull out the boards only
    best = []
    for i in range(min(k, len(scored))):
        best.append(scored[i][1])

    return best


#local beam search
#keep k states at once and update together
def run_local_beam_search(n, k=5, max_steps=2000):
    start_time = time.perf_counter()

    #start with k random boards
    beam = []
    for i in range(k):
        beam.append(make_random_board(n))

    steps_taken = 0

    #track best board seen so far
    best_board = None
    best_score = None

    while steps_taken < max_steps:

        '''
        finding way to drop runtime
        #update best seen
        for b in beam:
            s = get_conflicts(b)
            if best_score is None or s < best_score:
                best_score = s
                best_board = b
                '''

        for b in beam:
            s = get_conflicts(b)


            if best_score is None:
                best_score = s
                best_board = b
            elif s < best_score:
                best_score = s
                best_board = b
        #if solved stop
        if best_score == 0:
            break

        #generate all successors from all k boards
        all_successors = []

        for b in beam:
            neighbors = get_all_neighbors(b)
            for nb in neighbors:
                all_successors.append(nb)

        #if something weird happens
        if len(all_successors) == 0:
            break

        #keep only best k boards for next beam
        beam = keep_best_k(all_successors, k)

        steps_taken += 1

    end_time = time.perf_counter()
    run_time = end_time - start_time

    result_info = {
        "final_board": best_board,
        "final_conflicts": best_score,
        "steps": steps_taken,
        "solved": (best_score == 0),
        "runtime_seconds": run_time,
        "k_value": k
    }

    return result_info


#run trials for beam search
def run_beam_trials(n, number_of_runs=50, k=5, max_steps=2000, seed_value=0):
    random.seed(seed_value)

    solved_counter = 0
    total_steps_all = 0
    total_conflicts_all = 0
    total_time_all = 0.0

    all_results = []

    for i in range(number_of_runs):
        out = run_local_beam_search(n, k, max_steps)

        all_results.append(out)

        if out["solved"]:
            solved_counter += 1

        total_steps_all += out["steps"]
        total_conflicts_all += out["final_conflicts"]
        total_time_all += out["runtime_seconds"]

    summary_data = {
        "algorithm": "local_beam_search",
        "n_value": n,
        "runs": number_of_runs,
        "max_steps": max_steps,
        "seed": seed_value,
        "k_value": k,
        "success_rate": solved_counter / number_of_runs,
        "average_steps": total_steps_all / number_of_runs,
        "average_final_conflicts": total_conflicts_all / number_of_runs,
        "average_runtime_seconds": total_time_all / number_of_runs
    }

    return summary_data, all_results