<script>
  import CosmicHeistGame from './CosmicHeistGame.svelte';
  import { onMount } from 'svelte';

  // Define the list of possible symbols.  These strings must match the keys
  // used in the math configuration.  We include the special symbols here
  // so they can randomly appear on the board and trigger features.
  const SYMBOLS = [
    'SPACE_OUTLAW',
    'SPACESHIP',
    'LASER_GUN',
    'TREASURE_CHEST',
    'HOLO_MAP',
    'A', 'K', 'Q', 'J', 'TEN',
    'COSMIC_WILD',
    'GALACTIC_VAULT',
    'HEIST_TARGET'
  ];

  // Approximate weighting for each symbol.  Low‑pay symbols appear more
  // frequently than high‑pay symbols; wild, scatter and bonus symbols are
  // relatively rare.  Adjust these values to achieve your desired hit rates.
  const WEIGHTS = {
    SPACE_OUTLAW: 2,
    SPACESHIP: 3,
    LASER_GUN: 4,
    TREASURE_CHEST: 5,
    HOLO_MAP: 6,
    A: 10,
    K: 10,
    Q: 10,
    J: 12,
    TEN: 12,
    COSMIC_WILD: 2,
    GALACTIC_VAULT: 1,
    HEIST_TARGET: 1
  };

  // Build a flattened array of symbols repeated according to their weight.
  const weightedBag = [];
  for (const sym of SYMBOLS) {
    for (let i = 0; i < WEIGHTS[sym]; i++) weightedBag.push(sym);
  }

  function randomSymbol() {
    return weightedBag[Math.floor(Math.random() * weightedBag.length)];
  }

  function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  // Generate a new 4×5 board of random symbols.  Each column is a reel.
  function generateBoard() {
    const rows = 4;
    const cols = 5;
    const board = [];
    for (let r = 0; r < rows; r++) {
      const row = [];
      for (let c = 0; c < cols; c++) {
        row.push(randomSymbol());
      }
      board.push(row);
    }
    return board;
  }

  // Component state
  let board = generateBoard();
  let freeSpinsLeft = 0;
  let spinning = false;
  let bonusActive = false;
  let bonusChoices = [];
  let bonusResult = null;
  let message = '';

  // Apply the Quantum Wilds feature: randomly select 2–5 positions on the
  // board and transform them into wilds.  This happens on every spin.
  function applyQuantumWilds(board) {
    const count = randomInt(2, 5);
    const positions = [];
    // Build a list of all positions (row, col) pairs
    for (let r = 0; r < board.length; r++) {
      for (let c = 0; c < board[r].length; c++) {
        positions.push([r, c]);
      }
    }
    // Shuffle the positions and pick the first `count`
    positions.sort(() => Math.random() - 0.5);
    for (let i = 0; i < count; i++) {
      const [r, c] = positions[i];
      board[r][c] = 'COSMIC_WILD';
    }
  }

  // Apply expanding wilds during free spins: if a COSMIC_WILD appears on
  // any position of a reel, fill the entire reel with wilds.
  function applyExpandingWilds(board) {
    const rows = board.length;
    const cols = board[0].length;
    for (let c = 0; c < cols; c++) {
      let hasWild = false;
      for (let r = 0; r < rows; r++) {
        if (board[r][c] === 'COSMIC_WILD') {
          hasWild = true;
          break;
        }
      }
      if (hasWild) {
        for (let r = 0; r < rows; r++) {
          board[r][c] = 'COSMIC_WILD';
        }
      }
    }
  }

  // Check for scatter and bonus triggers after a spin.  Returns an object
  // describing whether free spins or bonus games should start.
  function checkTriggers(board) {
    let scatterCount = 0;
    let bonusCount = 0;
    for (const row of board) {
      for (const sym of row) {
        if (sym === 'GALACTIC_VAULT') scatterCount++;
        if (sym === 'HEIST_TARGET') bonusCount++;
      }
    }
    return { scatterCount, bonusCount };
  }

  // Start the grand heist bonus.  Five vaults appear, but only one can be
  // selected.  Each vault has a hidden multiplier drawn from the set
  // defined here; in a real game you would likely weight the values.
  function startBonusGame() {
    bonusActive = true;
    bonusResult = null;
    // Multipliers available; we pad the list to 5 items by repeating the
    // highest values to make the experience more exciting.
    const multipliers = [10, 20, 50, 100, 1000, 10000];
    // Randomly pick 5 multipliers from the list
    bonusChoices = [];
    while (bonusChoices.length < 5) {
      const m = multipliers[Math.floor(Math.random() * multipliers.length)];
      bonusChoices.push(m);
    }
  }

  // Handle selecting a vault.  Reveals the multiplier and ends the bonus.
  function selectVault(index) {
    bonusResult = bonusChoices[index];
    bonusActive = false;
    message = `Bonus won: ${bonusResult}×`;
  }

  // Spin the reels.  Handles both base and free spin modes.  If bonus is
  // active no spin is allowed until the player picks a vault.
  function spin() {
    if (spinning || bonusActive) return;
    spinning = true;
    message = '';
    // Decrement free spin counter if in free game
    if (freeSpinsLeft > 0) {
      freeSpinsLeft--;
    }
    // Generate a new board
    board = generateBoard();
    // Apply random wild transformations
    applyQuantumWilds(board);
    // During free spins, expand wilds to fill entire reels
    if (freeSpinsLeft > 0) {
      applyExpandingWilds(board);
    }
    // Check for triggers
    const { scatterCount, bonusCount } = checkTriggers(board);
    if (scatterCount >= 3) {
      // Award 8 free spins plus 2 extra per scatter beyond 3
      freeSpinsLeft += 8 + (scatterCount - 3) * 2;
      message = `Triggered ${8 + (scatterCount - 3) * 2} free spins!`;
    }
    if (bonusCount >= 3) {
      startBonusGame();
    }
    spinning = false;
  }

  // Automatically spin if free spins are active and no bonus is blocking
  $: if (freeSpinsLeft > 0 && !spinning && !bonusActive) {
    // Allow the UI to update before calling spin again
    setTimeout(() => spin(), 800);
  }
</script>

<style>
  .controls {
    margin-top: 1rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
  }
  button.spin {
    padding: 0.6rem 1.2rem;
    font-size: 1rem;
    border: none;
    border-radius: 4px;
    background-color: #5a56ff;
    color: #fff;
    cursor: pointer;
    transition: background 0.2s;
  }
  button.spin:hover {
    background-color: #837fff;
  }
  .free-spins {
    color: #0ff;
  }
  .bonus-vaults {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 1rem;
  }
  .vault {
    width: 80px;
    height: 80px;
    background-color: #222;
    border: 2px solid #555;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-weight: bold;
    cursor: pointer;
    user-select: none;
  }
  .message {
    color: #ffa600;
    font-weight: bold;
    margin-top: 0.5rem;
  }
</style>

<div>
  <CosmicHeistGame {board} />
  <div class="controls">
    <button class="spin" on:click={spin} disabled={spinning || bonusActive}>Spin{#if freeSpinsLeft > 0} (Free){/if}</button>
    {#if freeSpinsLeft > 0}
      <div class="free-spins">Free spins left: {freeSpinsLeft}</div>
    {/if}
    {#if message}
      <div class="message">{message}</div>
    {/if}
  </div>
  {#if bonusActive}
    <div class="bonus-vaults">
      {#each bonusChoices as val, idx}
        <div class="vault" on:click={() => selectVault(idx)}>
          &#128273;
        </div>
      {/each}
    </div>
    <div class="message">Pick a vault!</div>
  {/if}
  {#if bonusResult}
    <div class="message">You won {bonusResult}× on the heist!</div>
  {/if}
</div>