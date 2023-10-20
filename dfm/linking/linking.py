import yaml
import os

from dfm.linking.ignore import Ignore


class Linker:
    def __init__(self, src, dest, ignored, linked_dirs):
        self.src_dir = src
        self.dest_dir = dest
        self.ignored = ignored
        self.linked_dirs = linked_dirs


    @classmethod
    def load_config(cls, src, dest):
        with open(os.path.join(src, ".dfm.yaml"), "r") as cfg:
            config = yaml.safe_load(cfg)
            config["ignored"].append(r"\.dfm\.yaml")
            
        ignored = Ignore.from_config(config)
        linked_dirs = config["link_as_dir"]
        
        return cls(src, dest, ignored, linked_dirs) 


    def make_path_relative(self, abs_path, relative_to):
        return abs_path[len(relative_to)+1:]


    def link_profile(self):
        repo = os.path.abspath(self.src_dir)
        for root, dirnames, filenames in os.walk(repo):
            if ".git" in dirnames:
                dirnames.remove(".git")

            if any(root.endswith(d) for d in self.linked_dirs):
                self.make_link(root, repo)

            for filename in filenames:
                src = os.path.join(root, filename)
                self.make_link(src, repo)


    def link_to_homedir(self):
        target = os.path.join(os.path.expanduser("~"), self.dest_dir)
        if os.path.exists(target):
            return
        
        os.makedirs(os.path.dirname(target), exist_ok=True)
        os.symlink(self.src_dir, target)


    def make_link(self, abs_path: str, repo: str,):
        rel_path = self.make_path_relative(abs_path, repo)
        print(f"linking {abs_path} in to homedir at {rel_path}")
        if self.ignored.is_ignored(rel_path):
            return
        self.link_to_homedir()
