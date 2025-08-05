"""Entry point for simulating the Cosmic Heist slot.

This script demonstrates how the Cosmic Heist math model could be executed
using the Math SDK.  It mirrors the structure described in the quickstart
guide【915139723283763†L92-L107】, setting up a simulation of base and free spins
and producing human‑readable output.  In a real project you would run
many millions of simulations to generate the CSV lookup tables required
by Stake’s Remote Gaming Server.
"""

from __future__ import annotations

import json
from pathlib import Path

from game_config import GameConfig


def main() -> None:
    # Instantiate the game configuration.  In the real math SDK this
    # would also create the associated GameState and executables via
    # dependency injection.
    config = GameConfig()

    # Placeholder: simulate a small number of spins.  Without the
    # underlying math engine this just prints out the configuration.
    print("Running Cosmic Heist simulation…")
    print(f"Game ID: {config.game_id}")
    print(f"RTP target: {config.rtp:.2%}")
    print(f"Paytable entries: {len(config.paytable)}")

    # In a complete implementation you would call something like:
    #    results = run_spin(config, num_spins=1_000_000)
    # then write out `library/books`, `lookup_tables` and `index` files.
    # For demonstration we write the config to a JSON file.
    output = {
        "game_id": config.game_id,
        "paytable": {f"{kind}x {sym}": val for (kind, sym), val in config.paytable.items()},
        "reel_lengths": {mode: {r: len(s) for r, s in strips.items()} for mode, strips in config.reels.items()},
    }
    out_path = Path(__file__).parent / "demo_config.json"
    with out_path.open("w", encoding="utf-8") as fh:
        json.dump(output, fh, indent=2)
    print(f"Wrote demo configuration to {out_path}")


if __name__ == "__main__":
    main()