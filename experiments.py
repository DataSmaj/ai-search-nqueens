
from ss_search import run_hill_climb_trials
from ss_search import run_sideways_trials
from ss_search import run_restart_trials
from ss_search import run_sa_trials
from pb_search_lb import run_beam_trials

#main runner for part 1
def main():
    n = 8
    runs = 50
    max_steps = 5000
    seed_value = 0

    #part1 basic
    s1, r1 = run_hill_climb_trials(n=n, number_of_runs=runs, max_steps=max_steps, seed_value=seed_value)
    print(s1)

    #part2 sideways
    s2, r2 = run_sideways_trials(n=n, number_of_runs=runs, max_steps=max_steps, sideways_limit=50,seed_value=seed_value)
    print(s2)

    #part2 random restart
    s3, r3 = run_restart_trials(n=n, number_of_runs=runs, max_steps=max_steps, restarts=20, seed_value=seed_value)
    print(s3)


    #fast cooling
    s_fast, r_fast = run_sa_trials(n=8, number_of_runs=50, max_steps=20000, start_temp=50.0, cooling_rate=0.98,seed_value=0)
    print(s_fast)

    #slow coling
    s_slow, r_slow = run_sa_trials(n=8, number_of_runs=50, max_steps=20000, start_temp=50.0, cooling_rate=0.995,seed_value=0)
    print(s_slow)

    #Part4 local beam
    s_beam5, _ = run_beam_trials(n=8, number_of_runs=50, k=5, max_steps=2000, seed_value=0)
    print(s_beam5)

    s_beam10, _ = run_beam_trials(n=8, number_of_runs=50, k=10, max_steps=2000, seed_value=0)
    print(s_beam10)

    summary, results = run_hill_climb_trials(
        n=n,
        number_of_runs=runs,
        max_steps=max_steps,
        seed_value=seed_value
    )

    print(summary)
    print(results[0])


if __name__ == "__main__":
    main()



