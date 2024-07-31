import argparse
import timeit
import subprocess
import statistics
import pathlib
from typing import List, Tuple
import importlib.util

from .git import GitWrapper

git = GitWrapper()

def load_benchmark_function(file_path: str) -> callable:
    spec = importlib.util.spec_from_file_location("bench", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "main")

def run_benchmark(commit: str, bench_file: str, repeat: int, times: int) -> Tuple[float, float, float]:
    git.checkout_commit(commit)
    bench_func = load_benchmark_function(bench_file)
    # This function is lifted from richbench
    # https://github.com/tonybaloney/rich-bench/blob/master/richbench/__main__.py
    results = timeit.repeat(bench_func, repeat=repeat, number=times)
    subprocess.run("git checkout main || git checkout master", shell=True, check=True, stdout = subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return min(results), max(results), statistics.mean(results), results

def main():
    parser = argparse.ArgumentParser(description="Benchmark performance of a function using git bisect")
    parser.add_argument("--start-commit", help="Starting git commit", required=True)
    parser.add_argument("--end-commit", default="HEAD", help="Ending git commit")
    parser.add_argument("--bench-file", default="run-bench.py", help="Path to the benchmark file (default: bench.py)")
    parser.add_argument("--repeat", type=int, default=5, help="Number of times to repeat the benchmark (default: 5)")
    parser.add_argument("--times", type=int, default=100, help="Number of times to run the benchmark function (default: 100)")
    args = parser.parse_args()

    commits = git.get_commit_list(args.start_commit, args.end_commit)
    commits.append(args.start_commit)

    for commit in commits:
        print(commit)
        min_time, max_time, mean_time, results = run_benchmark(commit, args.bench_file, args.repeat, args.times)
        msg = git.get_commit_msg(commit)
        print(f"{commit[:8]:<40} {msg} {min_time:<10.4f}{max_time:<10.4f}{mean_time:<10.4f} {results}")

    # Restore to the original branch (assuming it's main or master)
    subprocess.run("git checkout main || git checkout master", shell=True, check=True, stdout = subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    main()