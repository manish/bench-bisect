import subprocess
from typing import List, Tuple
import logging

class GitWrapper:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__ + '.GitWrapper')

    def get_commit_list(self, start_commit: str, end_commit: str) -> List[str]:
        cmd = f"git rev-list {start_commit}..{end_commit}"
        self.logger.debug(cmd)
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        self.logger.debug(result)
        return result.stdout.strip().split('\n')

    def checkout_commit(self, commit: str):
        cmd = f"git checkout {commit}"
        self.logger.debug(cmd)
        subprocess.run(cmd, shell=True, check=True, stdout = subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def get_commit_msg(self, commit: str):
        cmd = f"git rev-list --format=%B --max-count=1 {commit}"
        results = subprocess.run(cmd, capture_output=True, text=True, shell=True).stdout.split('\n')
        self.logger.debug(results)
        if results[0] == f"commit {commit}":
            return results[1]