import { vitePreprocess } from '@sveltejs/kit/vite';
import adapter from '@sveltejs/adapter-auto';

/**
 * SvelteKit configuration
 * See https://kit.svelte.dev/docs/configuration
 */
const config = {
  // Apply SvelteKit’s default preprocessors
  preprocess: vitePreprocess(),
  kit: {
    // Use the auto adapter which detects the target environment
    adapter: adapter(),
    files: {
      assets: 'static',
      lib: 'src/lib'
    }
  }
};

export default config;