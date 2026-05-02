import random
import math
import time

from n_queens import make_random_board
from n_queens import get_conflicts
from n_queens import get_all_neighbors
from n_queens import get_random_neighbor

#find the best neighbor by checking all neighbors
#ties broken randomly
def find_best_neighbor(current_board):
    current_score = get_conflicts(current_board)

    best_score_found = current_score
    best_boards = []

    #generate all neighbors
    neighbors = get_all_neighbors(current_board)

    #check each neighbor
    for nb in neighbors:
        nb_score = get_conflicts(nb)

        #strict improvement
        if nb_score < best_score_found:
            best_score_found = nb_score
            best_boards = [nb]

        #tie for best
        elif nb_score == best_score_found:
            best_boards.append(nb)

    #if nothing improved at all
    if len(best_boards) == 0:
        return current_board, current_score

    chosen_board = random.choice(best_boards)
    return chosen_board, best_score_found


#basic hill climbing
#stop when no better neighbor exists
def run_hill_climb(n, max_steps=10000):
    start_time = time.perf_counter()

    #start random
    board = make_random_board(n)
    score = get_conflicts(board)

    steps_taken = 0

    while steps_taken < max_steps:
        next_board, next_score = find_best_neighbor(board)

        #no improvement means stuck
        if next_score >= score:
            break

        board = next_board
        score = next_score
        steps_taken += 1

        #solved early
        if score == 0:
            break

    end_time = time.perf_counter()
    run_time = end_time - start_time

    result_info = {
        "final_board": board,
        "final_conflicts": score,
        "steps": steps_taken,
        "solved": (score == 0),
        "runtime_seconds": run_time
    }

    return result_info

#hill climbing with sideways moves
#lets you move on flat areas for a limited number of steps
def run_hill_climb_sideways(n, max_steps=10000, sideways_limit=100):
    start_time = time.perf_counter()

    board = make_random_board(n)
    score = get_conflicts(board)

    steps_taken = 0
    sideways_used = 0

    while steps_taken < max_steps:

        next_board, next_score = find_best_neighbor(board)

        #if improvement then take it
        if next_score < score:
            board = next_board
            score = next_score
            steps_taken += 1
            sideways_used = 0

        #if equal score this is sideways move
        elif next_score == score:
            #only allow limited sideways steps
            if sideways_used >= sideways_limit:
                break

            board = next_board
            score = next_score
            steps_taken += 1
            sideways_used += 1

        #worse means stuck
        else:
            break

        if score == 0:
            break

    end_time = time.perf_counter()
    run_time = end_time - start_time

    result_info = {
        "final_board": board,
        "final_conflicts": score,
        "steps": steps_taken,
        "solved": (score == 0),
        "runtime_seconds": run_time,
        "sideways_limit": sideways_limit
    }

    return result_info


#random restart hill climbing
#run hill climb many times and keep best result
def run_random_restart_hill_climb(n, restarts=20, max_steps=10000):
    start_time = time.perf_counter()

    best_result = None

    #keep track because report will ask about behavior
    restart_counter = 0

    while restart_counter < restarts:
        out = run_hill_climb(n, max_steps)

        #first run just set it
        if best_result is None:
            best_result = out
        else:
            #keep the better solution
            if out["final_conflicts"] < best_result["final_conflicts"]:
                best_result = out

        #if solved we can stop early
        if out["solved"]:
            best_result = out
            break

        restart_counter += 1

    end_time = time.perf_counter()
    total_time = end_time - start_time

    #override time so it reflects the full restart process
    best_result = best_result.copy()
    best_result["runtime_seconds"] = total_time
    best_result["restarts_allowed"] = restarts
    best_result["restarts_used"] = restart_counter + 1

    return best_result


#trials for sideways hill climbing
def run_sideways_trials(n, number_of_runs=50, max_steps=10000, sideways_limit=100, seed_value=0):
    random.seed(seed_value)

    solved_counter = 0
    total_steps_all = 0
    total_conflicts_all = 0
    total_time_all = 0.0

    all_results = []

    for i in range(number_of_runs):
        out = run_hill_climb_sideways(n, max_steps, sideways_limit)

        all_results.append(out)

        if out["solved"]:
            solved_counter += 1

        total_steps_all += out["steps"]
        total_conflicts_all += out["final_conflicts"]
        total_time_all += out["runtime_seconds"]

    summary_data = {
        "algorithm": "hill_climb_sideways",
        "n_value": n,
        "runs": number_of_runs,
        "max_steps": max_steps,
        "seed": seed_value,
        "sideways_limit": sideways_limit,
        "success_rate": solved_counter / number_of_runs,
        "average_steps": total_steps_all / number_of_runs,
        "average_final_conflicts": total_conflicts_all / number_of_runs,
        "average_runtime_seconds": total_time_all / number_of_runs
    }

    return summary_data, all_results


#trials for random restart hill climbing
def run_restart_trials(n, number_of_runs=50, max_steps=10000, restarts=20, seed_value=0):
    random.seed(seed_value)

    solved_counter = 0
    total_steps_all = 0
    total_conflicts_all = 0
    total_time_all = 0.0

    all_results = []

    for i in range(number_of_runs):
        out = run_random_restart_hill_climb(n, restarts, max_steps)

        all_results.append(out)

        if out["solved"]:
            solved_counter += 1

        total_steps_all += out["steps"]
        total_conflicts_all += out["final_conflicts"]
        total_time_all += out["runtime_seconds"]

    summary_data = {
        "algorithm": "hill_climb_random_restart",
        "n_value": n,
        "runs": number_of_runs,
        "max_steps": max_steps,
        "seed": seed_value,
        "restarts": restarts,
        "success_rate": solved_counter / number_of_runs,
        "average_steps": total_steps_all / number_of_runs,
        "average_final_conflicts": total_conflicts_all / number_of_runs,
        "average_runtime_seconds": total_time_all / number_of_runs
    }

    return summary_data, all_results

#run repaeted trials for hill climbing
#for part 1 experiments
def run_hill_climb_trials(n, number_of_runs=50, max_steps=10000, seed_value=0):
    random.seed(seed_value)

    solved_counter = 0
    total_steps_all = 0
    total_conflicts_all = 0
    total_time_all = 0.0

    all_results = []

    for i in range(number_of_runs):
        out = run_hill_climb(n, max_steps)

        all_results.append(out)

        if out["solved"]:
            solved_counter += 1

        total_steps_all += out["steps"]
        total_conflicts_all += out["final_conflicts"]
        total_time_all += out["runtime_seconds"]

    summary_data = {
        "algorithm": "hill_climb",
        "n_value": n,
        "runs": number_of_runs,
        "max_steps": max_steps,
        "seed": seed_value,
        "success_rate": solved_counter / number_of_runs,
        "average_steps": total_steps_all / number_of_runs,
        "average_final_conflicts": total_conflicts_all / number_of_runs,
        "average_runtime_seconds": total_time_all / number_of_runs
    }

    return summary_data, all_results


#simulated annealing
#sometimes accepts worse moves depending on temp
def run_simulated_annealing(n, max_steps=20000, start_temp=50.0, cooling_rate=0.995):
    start_time = time.perf_counter()

    board = make_random_board(n)
    score = get_conflicts(board)

    temp = start_temp
    steps_taken = 0

    while steps_taken < max_steps and temp > 0.000001:

        #pick a random neighbor instead of best neighbor
        next_board = get_random_neighbor(board)
        next_score = get_conflicts(next_board)

        #delta is change in conflicts
        #negative delta is good (less conflicts)
        delta = next_score - score

        #if better always accept
        if delta < 0:
            board = next_board
            score = next_score

        else:
            #if worse maybe accept based on probability
            #prob = e^(-delta/temp)
            prob = math.exp(-delta / temp)
            roll = random.random()

            if roll < prob:
                board = next_board
                score = next_score

        steps_taken += 1

        #cool down temp
        temp = temp * cooling_rate

        if score == 0:
            break

    end_time = time.perf_counter()
    run_time = end_time - start_time

    result_info = {
        "final_board": board,
        "final_conflicts": score,
        "steps": steps_taken,
        "solved": (score == 0),
        "runtime_seconds": run_time,
        "start_temp": start_temp,
        "cooling_rate": cooling_rate
    }

    return result_info


#trials for simulated annealing
def run_sa_trials(n, number_of_runs=50, max_steps=20000, start_temp=50.0, cooling_rate=0.995, seed_value=0):
    random.seed(seed_value)

    solved_counter = 0
    total_steps_all = 0
    total_conflicts_all = 0
    total_time_all = 0.0

    all_results = []

    for i in range(number_of_runs):
        out = run_simulated_annealing(n, max_steps, start_temp, cooling_rate)

        all_results.append(out)

        if out["solved"]:
            solved_counter += 1

        total_steps_all += out["steps"]
        total_conflicts_all += out["final_conflicts"]
        total_time_all += out["runtime_seconds"]

    summary_data = {
        "algorithm": "simulated_annealing",
        "n_value": n,
        "runs": number_of_runs,
        "max_steps": max_steps,
        "seed": seed_value,
        "start_temp": start_temp,
        "cooling_rate": cooling_rate,
        "success_rate": solved_counter / number_of_runs,
        "average_steps": total_steps_all / number_of_runs,
        "average_final_conflicts": total_conflicts_all / number_of_runs,
        "average_runtime_seconds": total_time_all / number_of_runs
    }

    return summary_data, all_results

#basic stats for later tables
def get_min_max(values):
    if len(values) == 0:
        return None, None
    return min(values), max(values)