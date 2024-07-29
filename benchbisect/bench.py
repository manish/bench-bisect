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

def get_commit_list(start_commit: str, end_commit: str) -> List[str]:
    cmd = f"git rev-list {start_commit}..{end_commit}"
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return result.stdout.strip().split('\n')

def checkout_commit(commit: str):
    subprocess.run(f"git checkout {commit}", shell=True, check=True)

def load_benchmark_function(file_path: str) -> callable:
    spec = importlib.util.spec_from_file_location("bench", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "main")

def run_benchmark(commit: str, bench_file: str, repeat: int, times: int) -> Tuple[float, float, float]:
    checkout_commit(commit)
    bench_func = load_benchmark_function(bench_file)
    results = benchmark_function(bench_func, pathlib.Path('.'), repeat, times)
    return min(results), max(results), statistics.mean(results)

def main():
    parser = argparse.ArgumentParser(description="Benchmark Bisect")
    parser.add_argument("start_commit", help="Starting git commit")
    parser.add_argument("end_commit", help="Ending git commit")
    parser.add_argument("--bench-file", default="run-bench.py", help="Path to the benchmark file (default: bench.py)")
    parser.add_argument("--repeat", type=int, default=5, help="Number of times to repeat the benchmark (default: 5)")
    parser.add_argument("--times", type=int, default=100, help="Number of times to run the benchmark function (default: 100)")
    args = parser.parse_args()

    commits = get_commit_list(args.start_commit, args.end_commit)
    
    print(f"{'Commit':<40}{'Min':<10}{'Max':<10}{'Mean':<10}")
    print("-" * 70)

    for commit in commits:
        min_time, max_time, mean_time = run_benchmark(commit, args.bench_file, args.repeat, args.times)
        print(f"{commit[:8]:<40}{min_time:<10.4f}{max_time:<10.4f}{mean_time:<10.4f}")

    # Restore to the original branch (assuming it's main or master)
    subprocess.run("git checkout main || git checkout master", shell=True, check=True)

if __name__ == "__main__":
    main()