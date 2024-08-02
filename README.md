## Overview

Ever wanted to understand which git commit caused a performance regression for a specific code path?
The process can be tedious if you do not have the right tools. You have to write a benchmark function
and run it for every commit, capture the data, compare them and come to a conclusion.

What if it all happens for you? You provide a benchmark file with `main` as the entry method.
Then you specify the start commit and optionally end commit.

Sit back and relax and you will get the results saved as json to your disk and additionally a chart generated for you to look through and come to the conclusion.

[Example Plot](assets/sample_benchmark_results_plot.png)

By default it doesn't run git bisect, but runs benchmarks across all the commits

## Install

```bash
pip install benchbisect
```

This installs a tool in your pip package archive

## Usage

```bash
$ benchbisect --start-commit f8d889967c966a42b7e07df58a2441d11b489f6b
2024-08-01 23:18:33,920 - benchbisect.engine.ExecutionEngine - INFO - Starting benchmark process
2024-08-01 23:18:33,934 - benchbisect.bench.Benchmark - INFO - Running benchmark for commit 0b80be7c
2024-08-01 23:18:34,579 - benchbisect.bench.Benchmark - INFO - Running benchmark for commit 266dae7f
2024-08-01 23:18:34,927 - benchbisect.bench.Benchmark - INFO - Running benchmark for commit b2b9bb02
2024-08-01 23:18:35,259 - benchbisect.bench.Benchmark - INFO - Running benchmark for commit 339ded15
2024-08-01 23:18:35,372 - benchbisect.bench.Benchmark - INFO - Running benchmark for commit 43e1ee41
2024-08-01 23:18:36,418 - benchbisect.bench.Benchmark - INFO - Running benchmark for commit f8d88996
2024-08-01 23:18:36,824 - benchbisect.engine.ExecutionEngine - INFO - Saving benchmark results to file benchmark_results.json
2024-08-01 23:18:38,385 - benchbisect.plot.PlotBenchmarkResults - INFO - Plot saved to benchmark_results_plot.png
```

The benchmark function resides by default in `run-bench.py` file with `main` as entry method

This is how a sample `run-bench.py` file can look like

```py
from mypackage.critical import expensive_operation

def main():
    # This is the function that will be benchmarked
    result = expensive_operation()
    return result
```

If your benchmark file is named differently, then just use `--bench-file` to specify it.

## Help

```bash
benchbisect -h
usage: benchbisect [-h] --start-commit START_COMMIT [--end-commit END_COMMIT] [--bench-file BENCH_FILE]
                   [--json-output-file JSON_OUTPUT_FILE] [--repeat REPEAT] [--times TIMES] [--debug]
                   [--git-msg-on-plot]

Benchmark performance of a function using git bisect

options:
  -h, --help            show this help message and exit
  --start-commit START_COMMIT
                        Starting git commit
  --end-commit END_COMMIT
                        Ending git commit
  --bench-file BENCH_FILE
                        Path to the benchmark file (default: bench.py)
  --json-output-file JSON_OUTPUT_FILE
                        The file to write benchmark results
  --repeat REPEAT       Number of times to repeat the benchmark (default: 5)
  --times TIMES         Number of times to run the benchmark function (default: 100)
  --debug               Enable debug logging
  --git-msg-on-plot     Show git commit message on plot X axis
```