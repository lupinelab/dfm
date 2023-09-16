import click
import os
import functools
import json
import shutil
import sys
from xdg_base_dirs import xdg_state_home

from dfm.linking.linking import link_profile


def stateful(fn):
    @functools.wraps(fn)
    def __deco(*args, **kwargs):
        state_path = os.path.join(xdg_state_home(), "dfm", "state.json")
        try:
            with open(state_path) as fh:
                state = json.load(fh)
        except FileNotFoundError:
            state = {}

        kwargs["state"] = state
        fn(*args, **kwargs)
        os.makedirs(os.path.dirname(state_path), exist_ok=True)
        with open(state_path, "w") as fh:
            json.dump(state, fh)

    return __deco


@click.group()
def cli():
    pass


@cli.command()
@stateful
@click.argument("repo", nargs=-1)
def link(repo, state):
    profile = repo[0] if repo else state["current_profile"]
    link_profile(profile)
    state["current_profile"] = profile


@cli.command()
@stateful
@click.argument("path")
@click.option("-p", "--profile", type=str, default="")
def add(path, profile, state):
    if not profile:
        profile = state.get("current_profile")
    
    assert profile, "Bleurg, need profile!!!"
    abs_path = os.path.abspath(path)
    rel_path = os.path.relpath(abs_path, os.path.expanduser("~"))
    if os.path.isdir(abs_path):
        print("To add a directory do it manually")
        sys.exit(1)

    if os.path.islink(abs_path):
        return

    target_path = os.path.join(profile, rel_path)
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    shutil.copy2(abs_path, target_path)
    os.remove(abs_path)
    print(f"Added to {profile}, you should probably run `dfm link`!")
