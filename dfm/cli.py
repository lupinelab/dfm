import click
import os
import functools
import json
import shutil
import subprocess
import sys
from xdg_base_dirs import xdg_state_home

from dfm.profiles import Profile


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
@click.argument("profile", nargs=-1)
def link(profile, state):
    profile = Profile(profile or state.get("current_profile"))
    profile.link()
    state["current_profile"] = profile.repo


@cli.command()
@stateful
@click.argument("path")
@click.option("-p", "--profile", type=str, default="")
def add(path, profile, state):
    profile = Profile(profile or state.get("current_profile"))
    assert profile, "Bleurg, need profile!!!"
    profile.add(path)
    

@cli.command()
@stateful
@click.option("-p", "--profile", type=str, default="")
def sync(profile, state):
    profile = Profile(profile or state.get("current_profile"))
    profile.sync()


@cli.command(
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True
    )
)
@stateful
@click.option("-p", "--profile", type=str, default="")
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def git(profile, args, state):
    profile = Profile(profile or state.get("current_profile"))
    profile.git_cmd(args=list(args))
