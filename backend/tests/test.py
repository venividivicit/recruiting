#!/usr/bin/env python3

"""
NOTE: Test the simulator locally. First build the `queries` binary with `cargo build --release` and then run this script.
"""

from src.domain.modsim import data
from src.domain.simulator import Simulator
from src.domain.store import QRangeStore

store = QRangeStore()
sim = Simulator(store, data)
sim.simulate()
print(f"{len(store)=}")