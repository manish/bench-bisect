import subprocess
from typing import List, Tuple

class GitWrapper:
    def get_commit_list(self, start_commit: str, end_commit: str, debug=False) -> List[str]:
        cmd = f"git rev-list {start_commit}..{end_commit}"
        if debug:
            print(cmd)
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        if debug:
            print(result)
        return result.stdout.strip().split('\n')

    def checkout_commit(self, commit: str, debug=False):
        cmd = f"git checkout {commit}"
        if debug:
            print(cmd)
        subprocess.run(cmd, shell=True, check=True, stdout = subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def get_commit_msg(self, commit: str):
        cmd = f"git rev-list --format=%B --max-count=1 {commit}"
        results = subprocess.run(cmd, capture_output=True, text=True, shell=True).stdout.split('\n')
        print(results)
        if results[0] == f"commit {commit}":
            return results[1]