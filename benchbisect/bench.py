import argparse
import timeit
import subprocess
import statistics
import pathlib
from typing import List, Tuple
import importlib.util
from types import FunctionType
import pyinstrument

# This function is lifted from richbench
# https://github.com/tonybaloney/rich-bench/blob/master/richbench/__main__.py
def benchmark_function(func: FunctionType, bench_dir: pathlib.Path, repeat: int, times: int, profile=False):
    if profile:
        profiles_out = bench_dir / '.profiles'
        if not profiles_out.exists():
            profiles_out.mkdir(parents=True)
        profiler = pyinstrument.Profiler()
        profiler.start()

    result = timeit.repeat(func, repeat=repeat, number=times)

    if profile:
        profiler.stop()
        with open(profiles_out / f"{func.__name__}.html", "w", encoding='utf-8') as html:
            html.write(profiler.output_html())
    
    return result

def get_commit_list(start_commit: str, end_commit: str, debug=False) -> List[str]:
    cmd = f"git rev-list {start_commit}..{end_commit}"
    if debug:
        print(cmd)
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if debug:
        print(result)
    return result.stdout.strip().split('\n')

def checkout_commit(commit: str, debug=False):
    cmd = f"git checkout {commit}"
    if debug:
        print(cmd)
    subprocess.run(cmd, shell=True, check=True, stdout = subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def get_commit_msg(commit: str):
    cmd = f"git rev-list --format=%B --max-count=1 {commit}"
    results = subprocess.run(cmd, capture_output=True, text=True, shell=True).stdout.split('\n')
    print(results)
    if results[0] == f"commit {commit}":
        return results[1]

def load_benchmark_function(file_path: str) -> callable:
    spec = importlib.util.spec_from_file_location("bench", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "main")

def run_benchmark(commit: str, bench_file: str, repeat: int, times: int) -> Tuple[float, float, float]:
    checkout_commit(commit)
    bench_func = load_benchmark_function(bench_file)
    results = benchmark_function(bench_func, pathlib.Path('.'), repeat, times)
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

    commits = get_commit_list(args.start_commit, args.end_commit)
    commits.append(args.start_commit)

    for commit in commits:
        print(commit)
        min_time, max_time, mean_time, results = run_benchmark(commit, args.bench_file, args.repeat, args.times)
        msg = get_commit_msg(commit)
        print(f"{commit[:8]:<40} {msg} {min_time:<10.4f}{max_time:<10.4f}{mean_time:<10.4f} {results}")

    # Restore to the original branch (assuming it's main or master)
    subprocess.run("git checkout main || git checkout master", shell=True, check=True, stdout = subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    main()