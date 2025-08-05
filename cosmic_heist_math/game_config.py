"""Configuration for the Cosmic Heist slot game.

This module defines a `GameConfig` class inheriting from the base `Config`
class provided by the Stake Engine Math SDK.  It sets up the core
parameters for a 5×4 ways‑pay slot with high volatility and outlines where
feature logic should be implemented.  The values here are illustrative and
should be tuned through simulation to achieve the desired RTP (~96.5 %).

Note: The Carrot math engine uses classes such as `Config`, `BetMode` and
`Distribution` to structure a game【32421590752536†L86-L129】.  This file assumes that
those base classes are available on the Python path when run within the
math‑sdk environment.
"""
from __future__ import annotations

from typing import Dict, Tuple

try:
    # Import SDK base classes.  These imports will resolve when placed inside
    # the math-sdk repository.  They are provided here for reference.
    from src.config import Config
    from src.bet_mode import BetMode
    from src.distribution import Distribution
except ImportError:
    # During early development outside of the SDK, we define minimal stubs so
    # that type checkers don't complain.  When running inside the math‑sdk
    # environment these will be replaced by the actual implementations.
    class Config:
        def __init__(self):
            pass

    class BetMode:
        def __init__(self, *args, **kwargs):
            pass

    class Distribution:
        def __init__(self, *args, **kwargs):
            pass


class GameConfig(Config):
    """Configuration for the Cosmic Heist slot.

    The `GameConfig` holds all static parameters for the game: board size,
    symbol definitions, paytable, reel strips and free‑spin triggers.  It
    also defines the different betting modes (e.g. base game vs free spins)
    and sets up high‑level distribution rules controlling hit‑rates and
    maximum wins【32421590752536†L90-L177】.
    """

    def __init__(self) -> None:
        super().__init__()

        # Basic metadata
        self.game_id: str = "cosmic_heist"
        self.provider_number: int = 0  # Replace with your assigned provider ID
        self.working_name: str = "Cosmic Heist"
        self.wincap: float = 10000  # maximum win multiplier (e.g. 10,000×)
        self.win_type: str = "ways"  # use ways pay rather than lines【32421590752536†L90-L103】
        self.rtp: float = 0.965  # target return to player

        # Board dimensions: 5 reels with four rows each
        self.num_reels: int = 5
        self.num_rows: list[int] = [4] * self.num_reels

        # Paytable: map (kind, symbol) → payout multiplier
        # `kind` is the number of matching symbols on adjacent reels starting
        # from the leftmost reel.  `symbol` is an identifier from `self.symbols`.
        # Values here are indicative; you should adjust them through simulation.
        self.paytable: Dict[Tuple[int, str], float] = {
            # High‑pay symbols
            (5, "SPACE_OUTLAW"): 50.0,
            (4, "SPACE_OUTLAW"): 20.0,
            (3, "SPACE_OUTLAW"): 5.0,

            (5, "SPACESHIP"): 25.0,
            (4, "SPACESHIP"): 10.0,
            (3, "SPACESHIP"): 3.0,

            (5, "LASER_GUN"): 15.0,
            (4, "LASER_GUN"): 5.0,
            (3, "LASER_GUN"): 2.0,

            (5, "TREASURE_CHEST"): 12.0,
            (4, "TREASURE_CHEST"): 4.0,
            (3, "TREASURE_CHEST"): 1.5,

            (5, "HOLO_MAP"): 10.0,
            (4, "HOLO_MAP"): 3.0,
            (3, "HOLO_MAP"): 1.0,

            # Low‑pay symbols (card suits with neon theming)
            (5, "A"): 5.0,
            (4, "A"): 2.5,
            (3, "A"): 0.5,

            (5, "K"): 4.0,
            (4, "K"): 2.0,
            (3, "K"): 0.4,

            (5, "Q"): 3.0,
            (4, "Q"): 1.5,
            (3, "Q"): 0.3,

            (5, "J"): 2.5,
            (4, "J"): 1.0,
            (3, "J"): 0.2,

            (5, "TEN"): 2.0,
            (4, "TEN"): 0.8,
            (3, "TEN"): 0.2,
        }

        # Control whether empty positions (padding) are included when building ways
        self.include_padding: bool = True

        # Special symbol definitions.  Here the key is a property name and the
        # value is a list of symbol identifiers which share that property.
        self.special_symbols: Dict[str, list[str]] = {
            # Wilds substitute for regular symbols but not scatters or bonuses.
            "wild": ["COSMIC_WILD"],
            # Scatter symbols trigger free spins.
            "scatter": ["GALACTIC_VAULT"],
            # Bonus symbols trigger the heist bonus game.
            "bonus": ["HEIST_TARGET"],
        }

        # Define triggers for free spins (Black Hole Respin feature).  When at
        # least three scatter symbols land anywhere on the board the game will
        # enter the free‑spin mode with an initial eight spins.  Additional
        # scatters award extra spins.  The free‑spin logic itself should be
        # implemented in your gamestate/executables.
        self.freespin_triggers: Dict[str, Dict[str, int]] = {
            # basegame → freegame
            "base": {"GALACTIC_VAULT": 3},
        }

        # Reel strips: define the order of symbols on each reel.  For a ways
        # game the reel strips control hit‑rates and symbol frequencies.  Use
        # duplicates to weight more common symbols.  Below is an illustrative
        # sequence; you should refine these values through simulation.
        self.reels: Dict[str, Dict[str, list[str]]] = {
            # Base game reels
            "base": {
                "R0": [
                    "SPACE_OUTLAW", "SPACESHIP", "LASER_GUN", "TREASURE_CHEST",
                    "HOLO_MAP", "A", "K", "Q", "J", "TEN",
                    "COSMIC_WILD", "GALACTIC_VAULT", "HEIST_TARGET",
                    # repeat low‑pay symbols for weighting
                    "A", "K", "Q", "J", "TEN", "A", "K", "Q", "J", "TEN",
                ],
                # Duplicate the same distribution for all reels for simplicity
                "R1": [],
                "R2": [],
                "R3": [],
                "R4": [],
            },
            # Freegame reels (can differ for increased volatility)
            "free": {
                "R0": [
                    "SPACE_OUTLAW", "SPACESHIP", "LASER_GUN", "TREASURE_CHEST",
                    "HOLO_MAP", "A", "K", "Q", "J", "TEN",
                    "COSMIC_WILD", "GALACTIC_VAULT", "HEIST_TARGET",
                    "COSMIC_WILD", "COSMIC_WILD",  # extra wilds in free spins
                    "GALACTIC_VAULT", "GALACTIC_VAULT",
                ],
                "R1": [],
                "R2": [],
                "R3": [],
                "R4": [],
            },
        }
        # Copy the base list into the other reels to keep weighting consistent
        for mode in self.reels:
            base_strip = self.reels[mode]["R0"]
            for r in ["R1", "R2", "R3", "R4"]:
                # Use list() to copy so mutations on one reel don’t affect the others
                self.reels[mode][r] = list(base_strip)

        # Define the game’s bet modes.  At minimum there is a base mode and a
        # free‑spin mode.  Each bet mode can have its own set of distribution
        # rules controlling hit‑rates and RTP allocation【32421590752536†L118-L177】.
        self.bet_modes: list[BetMode] = [
            BetMode(
                name="base",
                cost=1.0,
                rtp=self.rtp * 0.8,  # allocate 80 % of RTP to base game
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=False,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="feature",
                        quota=0.1,
                        conditions={"force_freegame": True},
                    ),
                    Distribution(
                        criteria="0",
                        quota=0.5,
                        win_criteria=0.0,
                        conditions={},
                    ),
                    Distribution(
                        criteria="basegame",
                        quota=0.4,
                        conditions={},
                    ),
                ],
            ),
            BetMode(
                name="free",
                cost=0.0,
                rtp=self.rtp * 0.2,  # allocate 20 % of RTP to free spins
                max_win=self.wincap,
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="freegame",
                        quota=1.0,
                        conditions={"force_freegame": True},
                    ),
                ],
            ),
        ]

        # Additional setup can be done here, such as setting up force files
        # for guaranteed feature triggers during testing.

    # ------------------------------------------------------------------
    # Below are placeholders for event hooks that you would implement in
    # the GameState and GameExecutables classes.  The math SDK expects
    # event logic to be defined outside of GameConfig, but these comments
    # indicate where the Cosmic Heist features would be handled.
    #
    # def on_spin_start(self):
    #     """Called before each spin.  Good place to reset temporary state."""
    #     pass
    #
    # def apply_quantum_wilds(self, board: list[list[str]]):
    #     """
    #     Randomly transforms 2–5 symbols into wilds on the current board.
    #     This should be called during base and free spins before win evaluation.
    #     """
    #     pass
    #
    # def enter_black_hole_respins(self):
    #     """
    #     Handles the free spins feature triggered by scatters.  Expanding wilds
    #     should be added to any reel where a wild lands, and retriggers
    #     should grant additional spins.
    #     """
    #     pass
    #
    # def enter_grand_heist_bonus(self):
    #     """
    #     Handles the interactive bonus game triggered by three or more
    #     HEIST_TARGET symbols.  The bonus game should present the player
    #     with several vaults containing multipliers up to 10 000×.  The
    #     selected multiplier becomes the payout for the bonus.
    #     """
    #     pass
