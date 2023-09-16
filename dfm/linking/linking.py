import yaml
import os

from dfm.linking.ignore import Ignore


def read_config(repo):
    ## check exists
    with open(os.path.join(repo, ".dfm2.yaml"), "r") as cfg:
        config = yaml.safe_load(cfg)
        config["ignored"].append(r"\.dfm2\.yaml")
        return config


def make_path_relative(abs_path, relative_to):
    return abs_path[len(relative_to)+1:]


def link_profile(profile):
    repo = os.path.abspath(profile)
    cfg = read_config(repo)
    ignored = Ignore.from_config(cfg)
    linked_dirs = cfg["link_as_dir"]
    for root, dirnames, filenames in os.walk(repo):
        if ".git" in dirnames:
            dirnames.remove(".git")

        if any(root.endswith(d) for d in linked_dirs):
            make_link(root, repo, ignored)

        for filename in filenames:
            src = os.path.join(root, filename)
            make_link(src, repo, ignored)


def link_to_homedir(src, rel_path):
    target = os.path.join(os.path.expanduser("~"), rel_path)
    if os.path.exists(target):
        return
    
    os.makedirs(os.path.dirname(target), exist_ok=True)
    os.symlink(src, target)


def make_link(abs_path: str, repo: str, ignored: Ignore):
    rel_path = make_path_relative(abs_path, repo)
    print(f"linking {abs_path} in to homedir at {rel_path}")
    if ignored.is_ignored(rel_path):
        return
    link_to_homedir(abs_path, rel_path)
