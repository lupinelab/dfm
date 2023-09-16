import re


class Ignore:
    @classmethod
    def from_config(cls, cfg):
        return cls(cfg["ignored"])

    def __init__(self, ignored_list: list[str]):
        self.ignored = [re.compile(ignore) for ignore in ignored_list]

    def is_ignored(self, rel_path: str):
        print(f"Checking if {rel_path} is ignored")
        return any(ignore.match(rel_path) for ignore in self.ignored)
