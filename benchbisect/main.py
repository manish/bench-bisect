import argparse
import logging

from .git import GitWrapper
from .engine import ExecutionEngine

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
    parser.add_argument("--git-msg-on-plot", action="store_true", help="Show git commit message on plot X axis")
    args = parser.parse_args()

    setup_logging(args.debug)

    engine = ExecutionEngine()
    engine.run(args)

if __name__ == "__main__":
    main()