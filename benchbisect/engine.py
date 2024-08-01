import logging
import subprocess
import json

from .git import GitWrapper
from .bench import Benchmark

class ExecutionEngine:
    def __init__(self):
        self.logger = logging.getLogger(__name__ + '.ExecutionEngine')
        self.git = GitWrapper()
        self.benchmark = Benchmark()

    def run(self, args):
        commits = self.get_all_commits(args.start_commit, args.end_commit)
        try:
            all_results=[]
            for idx, commit in enumerate(commits):
                processed_commit_output = self.process_commit(idx, commit, args.bench_file, args.repeat, args.times)
                all_results.append(processed_commit_output)
            
            self.save_results(all_results, args.json_output_file)
        finally:
            self.logger.debug("Restoring to original branch")
            subprocess.run("git checkout main || git checkout master", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def process_commit(self, idx, commit, bench_file, repeat, times):
        self.logger.debug(f"Processing commit: {commit}")
        min_time, max_time, mean_time, results = self.benchmark.run_benchmark(commit, bench_file, repeat, times)
        msg = self.git.get_commit_msg(commit)
        self.logger.debug(f"{commit[:8]:<40} {msg} {min_time:<10.4f}{max_time:<10.4f}{mean_time:<10.4f} {results}")
        return {
            "execution_order": idx,
            "commit": commit,
            "message": msg,
            "data": results,
            "minimum": min_time,
            "maximum": max_time,
            "mean": mean_time,
        }
    
    def save_results(self, all_results, json_output_file):
        self.logger.info(f"Saving benchmark results to file {json_output_file}")
        with open(json_output_file, 'w') as f:
            json.dump(all_results, f, indent=2)

    def get_all_commits(self, start_commit, end_commit):
        self.logger.info("Starting benchmark process")
        commits = self.git.get_commit_list(start_commit, end_commit)
        commits.append(start_commit)
        self.logger.debug(f"Commits to benchmark: {commits}")
        return commits