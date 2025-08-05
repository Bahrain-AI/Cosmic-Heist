# Cosmic Heist Math Model

This directory contains a skeleton implementation of the **Cosmic Heist** slot game's
math model using the [Stake Engine Math SDK]【452306070317762†L324-L331】.  The goal of this
model is to illustrate how you might set up a new game inside Stake’s
Python‑based math engine.  It is **not** a complete, production‑ready
implementation, but it provides a starting point for defining the
configuration, symbol set and feature logic for your game.

## Overview

* **Reels and Ways:** The game uses a 5‑reel, 4‑row board and pays on 1,024 ways to win.
* **Volatility:** High volatility, targeting an RTP of ~96.5 %.
* **Symbols:** The symbols and their approximate payout values are defined in
  [`game_config.py`](game_config.py).  Low‑tier symbols are stylised card suits
  (10–A) and high‑tier symbols are themed around an intergalactic heist.  The
  game also has special wild, scatter and bonus symbols.
* **Features:** The design includes three principal bonus features—
  *Quantum Wilds*, *Black Hole Respins* and the *Grand Heist Bonus*—each of
  which would be implemented as events in the math engine.  Comments in
  `game_config.py` outline where these hooks belong.

## Using the Math SDK

The Stake Engine math framework is a Python engine that generates all of the
files required to drive the Remote Gaming Server【635126774274739†L85-L105】.  It allows you to
define game parameters via a `GameConfig` class and to specify payout
distributions, reels and events.  Once a game is defined you can simulate
millions of spins to verify the RTP and hit‑rates, then publish the output
files for deployment.

To work with this skeleton you should have the Math SDK installed.  See the
official quickstart guide for details on setting up the engine and running
simulations【915139723283763†L92-L107】.

## Next steps

1. **Install the SDK:** Follow the setup instructions in the docs or run
   `make setup` from within the math‑sdk repository【452306070317762†L328-L344】.
2. **Create your game directory:** Copy or rename the `cosmic_heist_math`
   directory under the `games/` folder of the math SDK.
3. **Fill in the logic:** Implement the event handlers in
   `game_config.py` and associated state/executable files.  You can use
   existing examples (e.g., the `ways` sample) as a reference for how to
   implement ways‑pays and free spin logic.
4. **Simulate and iterate:** Use the `run.py` script to generate output
   files and iteratively adjust symbol weights and feature triggers until
   the desired RTP and volatility profile are reached.

For more detailed information on the available configuration options, refer
to the [Game Format] section of the math SDK documentation【32421590752536†L86-L119】.