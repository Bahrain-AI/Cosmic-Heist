<script>
  import GameController from '../components/GameController.svelte';
</script>

<style>
  main {
    padding: 2rem;
    font-family: sans-serif;
    color: #fff;
    background: radial-gradient(circle at center, #0d0f28 0%, #04050f 100%);
    min-height: 100vh;
  }
  h1 {
    text-align: center;
    margin-bottom: 1rem;
    font-size: 2rem;
    font-weight: 600;
  }
</style>

<main>
  <h1>Cosmic&nbsp;Heist Prototype</h1>
  <GameController />
</main>