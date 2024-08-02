import logging
import matplotlib.pyplot as plt

class PlotBenchmarkResults:
    def __init__(self, data, git_msg_on_plot) -> None:
        self.git_msg_on_plot = git_msg_on_plot
        self.logger = logging.getLogger(__name__ + '.PlotBenchmarkResults')
        self.commits = [item['commit'][:8] for item in data]  # Short commit hash
        self.means = [item['mean'] for item in data]
        self.mins = [item['minimum'] for item in data]
        self.maxs = [item['maximum'] for item in data]
        self.messages = [item['message'] for item in data]

    def plot(self, chart_file_name="benchmark_results_plot.png"):
        plt.figure(figsize=(12, 6))
        x_data = self.messages if self.git_msg_on_plot else self.commits
        plt.plot(x_data, self.means, 'o-', label='Mean', color='#1f77b4', linewidth=2, markersize=8)
        plt.plot(x_data, self.mins, 's-', label='Minimum', color='#2ca02c', linewidth=2, markersize=8)
        plt.plot(x_data, self.maxs, '^-', label='Maximum', color='#d62728', linewidth=2, markersize=8)
        plt.fill_between(x_data, self.mins, self.maxs, alpha=0.2, color='#1f77b4')

        plt.title('Benchmark Results Across Commits', fontsize=16)
        plt.xlabel('Commit Hash', fontsize=12)
        plt.ylabel('Execution Time (seconds)', fontsize=12)
        plt.legend(fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(chart_file_name, dpi=600, bbox_inches='tight')

        self.logger.info(f"Plot saved to {chart_file_name}")