<script>
  /**
   * CosmicHeistGame renders a 5×4 grid of symbols.  The component accepts a
   * `board` prop where each entry is a string matching one of the keys in
   * the `images` map.  This allows the math engine to drive the UI by
   * specifying which symbols appear in each position.
   */
  export let board = [
    ["SPACE_OUTLAW", "SPACESHIP", "LASER_GUN", "SPACE_OUTLAW", "SPACESHIP"],
    ["LASER_GUN", "SPACE_OUTLAW", "SPACESHIP", "LASER_GUN", "SPACE_OUTLAW"],
    ["SPACESHIP", "LASER_GUN", "SPACE_OUTLAW", "SPACESHIP", "LASER_GUN"],
    ["SPACE_OUTLAW", "SPACESHIP", "LASER_GUN", "SPACE_OUTLAW", "SPACESHIP"],
  ];

  // Import symbol images.  Replace these with your own assets as needed.
  import spaceOutlawImg from '../assets/space_outlaw.png';
  import spaceshipImg from '../assets/spaceship.png';
  import laserGunImg from '../assets/laser_gun.png';
  import treasureChestImg from '../assets/treasure_chest.png';
  import holographicMapImg from '../assets/holographic_map.png';
  import cosmicWildImg from '../assets/cosmic_wild.png';
  import galacticVaultImg from '../assets/galactic_vault.png';
  import heistTargetImg from '../assets/heist_target.png';
  import aImg from '../assets/A.png';
  import kImg from '../assets/K.png';
  import qImg from '../assets/Q.png';
  import jImg from '../assets/J.png';
  import tenImg from '../assets/TEN.png';

  const images = {
    SPACE_OUTLAW: spaceOutlawImg,
    SPACESHIP: spaceshipImg,
    LASER_GUN: laserGunImg,
    TREASURE_CHEST: treasureChestImg,
    HOLO_MAP: holographicMapImg,
    COSMIC_WILD: cosmicWildImg,
    GALACTIC_VAULT: galacticVaultImg,
    HEIST_TARGET: heistTargetImg,
    A: aImg,
    K: kImg,
    Q: qImg,
    J: jImg,
    TEN: tenImg,
  };
</script>

<style>
  .board {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    grid-template-rows: repeat(4, 1fr);
    gap: 0.4rem;
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
  }
  .cell {
    aspect-ratio: 1 / 1;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    overflow: hidden;
  }
  img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }
</style>

<div class="board">
  {#each board as row}
    {#each row as cell}
      <div class="cell">
        {#if images[cell]}
          <img src={images[cell]} alt={cell} />
        {:else}
          <!-- Unknown symbol placeholder -->
        {/if}
      </div>
    {/each}
  {/each}
</div>