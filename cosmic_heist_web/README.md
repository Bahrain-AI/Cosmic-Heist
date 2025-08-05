# Cosmic Heist Front‑End

This directory contains a very simple Svelte component to serve as a
starting point for building the **Cosmic Heist** slot’s user interface using
the Stake Engine web SDK.  The official web framework uses PixiJS in
combination with Svelte, as described in the SDK documentation【8940988072427†L75-L120】.  The
component here does not rely on any proprietary packages and instead
demonstrates how you might structure the reels and display symbol
graphics.

## Installation

To run the front‑end you need Node 18 and pnpm as outlined in the
stakeengine guide【8940988072427†L80-L102】.  Install the dependencies (including
the SvelteKit adapter) and start the dev server:

```bash
cd cosmic_heist_web
pnpm install
pnpm run dev
```

The project depends on **@sveltejs/adapter‑auto** for building and serving
the app.  If you encounter errors about a missing adapter when running
`pnpm install` or `pnpm run dev`, install it manually with
`pnpm add -D @sveltejs/adapter-auto` and then try again.  Once the
dependencies are installed, the command above will start a local
SvelteKit dev server; visit the printed URL in your browser to interact
with the prototype.

## Structure

* `src/assets/` contains image assets used by the game.  You should
  replace the placeholder images with your final art (see
  `../cosmic_heist_math/README.md` for asset guidelines).
* `src/components/CosmicHeistGame.svelte` is the main component that
  renders a 5×4 grid of symbols.  It accepts a `board` prop so that
  symbol identifiers from the math engine can be mapped to images.
* `src/routes/+page.svelte` instantiates the component with a dummy
  starting board.

In a complete implementation you would consume events from the RGS
(`play/` API) to update the board and animate spins.  See the Stake
Engine storybook for examples of how to use Pixi‑Svelte and XState to
manage state and animations.