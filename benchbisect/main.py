import argparse
import subprocess
import logging
import json

from .git import GitWrapper
from .bench import Benchmark

git = GitWrapper()

def setup_logging(debug: bool):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="Benchmark performance of a function using git bisect")
    parser.add_argument("--start-commit", help="Starting git commit", required=True)
    parser.add_argument("--end-commit", default="HEAD", help="Ending git commit")
    parser.add_argument("--bench-file", default="run-bench.py", help="Path to the benchmark file (default: bench.py)")
    parser.add_argument("--json-output-file", default="benchmark_results.json", help="The file to write benchmark results")
    parser.add_argument("--repeat", type=int, default=5, help="Number of times to repeat the benchmark (default: 5)")
    parser.add_argument("--times", type=int, default=100, help="Number of times to run the benchmark function (default: 100)")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    setup_logging(args.debug)
    logger = logging.getLogger(__name__)

    logger.info("Starting benchmark process")
    commits = git.get_commit_list(args.start_commit, args.end_commit)
    commits.append(args.start_commit)
    logger.debug(f"Commits to benchmark: {commits}")

    benchmark = Benchmark()

    try:
        all_results=[]
        for idx, commit in enumerate(commits):
            logger.debug(f"Processing commit: {commit}")
            min_time, max_time, mean_time, results = benchmark.run_benchmark(commit, args.bench_file, args.repeat, args.times)
            msg = git.get_commit_msg(commit)
            logger.debug(f"{commit[:8]:<40} {msg} {min_time:<10.4f}{max_time:<10.4f}{mean_time:<10.4f} {results}")
            all_results.append({
                "execution_order": idx,
                "commit": commit,
                "message": msg,
                "data": results,
                "minimum": min_time,
                "maximum": max_time,
                "mean": mean_time,
            })

        logger.info(f"Saving benchmark results to file {args.json_output_file}")
        with open(args.json_output_file, 'w') as f:
            json.dump(all_results, f, indent=2)
    finally:
        logger.debug("Restoring to original branch")
        subprocess.run("git checkout main || git checkout master", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    main()