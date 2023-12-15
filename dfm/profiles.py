import os
import shutil
import subprocess
import sys

from dfm.linking.linker import Linker


class Profile:
    def __init__(self, repo):
        self.repo = repo
        self.linker = Linker.load_config(repo, os.path.join(os.path.expanduser("~")))

    def add(self, filepath):
        abs_path = os.path.abspath(filepath)
        rel_path = os.path.relpath(abs_path, os.path.expanduser("~"))
        if os.path.isdir(abs_path):
            print("To add a directory do it manually")
            sys.exit(1)

        if os.path.islink(abs_path):
            return

        target_path = os.path.join(self.repo, rel_path)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        shutil.copy2(abs_path, target_path)
        os.remove(abs_path)
        print(f"Added to {self.repo}, you should probably run `dfm link`!")

    def git_cmd(self, args: list, capture: bool = False):
        return subprocess.run(
            ["git"] + args, cwd=self.repo, capture_output=capture, check=True
        )

    def is_dirty(self):
        status = self.git_cmd(args=["status", "--porcelain"], capture=True)
        return bool(status.stdout.decode("utf-8"))

    def commit_changes(self):
        self.git_cmd(args=["add", "--all"])
        self.git_cmd(args=["commit", "-m", "changes to dotfiles"])

    def update_profile(self):
        self.git_cmd(args=["push"])

    def receive_changes(self):
        self.git_cmd(args=["pull", "--rebase"])

    def sync(self):
        has_changes = self.is_dirty()
        if has_changes:
            print(f"{self.repo} has uncommited changes, committing...")
            self.commit_changes()

        print("Pulling changes from origin")
        self.receive_changes()

        if has_changes:
            print(f"Pushing changes to {self.repo}")
            self.update_profile()

    def link(self):
        self.linker.link_profile()
