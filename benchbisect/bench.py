import timeit
import subprocess
import statistics
import logging
from typing import List, Tuple
import importlib.util

from .git import GitWrapper

class Benchmark:
    def __init__(self):
        self.logger = logging.getLogger(__name__ + '.Benchmark')
        self.git = GitWrapper()

    def load_benchmark_function(self, file_path: str) -> callable:
        self.logger.debug(f"Loading benchmark function from {file_path}")
        spec = importlib.util.spec_from_file_location("bench", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, "main")

    def run_benchmark(self, commit: str, bench_file: str, repeat: int, times: int) -> Tuple[float, float, float, List[float]]:
        self.logger.info(f"Running benchmark for commit {commit}")
        self.git.checkout_commit(commit)
        bench_func = self.load_benchmark_function(bench_file)
        # This function is lifted from richbench
        # https://github.com/tonybaloney/rich-bench/blob/master/richbench/__main__.py
        results = timeit.repeat(bench_func, repeat=repeat, number=times)
        self.logger.debug(f"Benchmark results: {results}")
        subprocess.run("git checkout main || git checkout master", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return min(results), max(results), statistics.mean(results), results