#!/usr/bin/env python3
# -*- coding: utf8 -*-
# tab-width:4

from __future__ import annotations

import logging
from pathlib import Path
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal

import click
import sh
from asserttool import ic
from click_auto_help import AHGroup
from clicktool import click_add_options
from clicktool import click_global_options
from clicktool import tvicgvd
from globalverbose import gvd
from mounttool import block_special_path_is_mounted
from pathtool import path_is_block_special
from warntool import warn

logging.basicConfig(level=logging.INFO)
sh.mv = None  # use sh.busybox('mv'), coreutils ignores stdin read errors

# this should be earlier in the imports, but isort stops working
signal(SIGPIPE, SIG_DFL)


@click.group(no_args_is_help=True, cls=AHGroup)
@click_add_options(click_global_options)
@click.pass_context
def cli(
    ctx,
    verbose_inf: bool,
    dict_output: bool,
    verbose: bool = False,
) -> None:
    tty, verbose = tvicgvd(
        ctx=ctx,
        verbose=verbose,
        verbose_inf=verbose_inf,
        ic=ic,
        gvd=gvd,
    )


@cli.command()
@click.argument(
    "device",
    type=click.Path(
        exists=True,
        dir_okay=False,
        file_okay=True,
        allow_dash=False,
        path_type=Path,
    ),
    nargs=1,
    required=True,
)
@click.argument(
    "label",
    type=click.Choice(
        [
            "aix",
            "amiga",
            "bsd",
            "dvh",
            "gpt",
            "mac",
            "msdos",
            "pc98",
            "sun",
            "atari",
            "loop",
        ]
    ),
    nargs=1,
)
@click.option("--force", is_flag=True)
@click_add_options(click_global_options)
@click.pass_context
def write(
    ctx,
    device: Path,
    label: str,
    force: bool,
    verbose_inf: bool,
    dict_output: bool,
    verbose: bool = False,
) -> None:
    tty, verbose = tvicgvd(
        ctx=ctx,
        verbose=verbose,
        verbose_inf=verbose_inf,
        ic=ic,
        gvd=gvd,
    )

    assert path_is_block_special(device, symlink_ok=True)
    assert not block_special_path_is_mounted(
        device,
    )
    if not force:
        warn(
            (device,),
            symlink_ok=True,
        )

    parted_command = sh.Command("parted")
    parted_command = parted_command.bake(device.as_posix())
    parted_command = parted_command.bake(
        "--script",
        "--",
        "mklabel",
        label,
    )
    result = parted_command()
