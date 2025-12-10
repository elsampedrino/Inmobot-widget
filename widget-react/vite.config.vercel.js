// vite.config.vercel.js - Configuración para deployment en Vercel
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  define: {
    'process.env.NODE_ENV': '"production"'
  },
  build: {
    // NO usar modo lib - generar sitio web completo
    outDir: 'dist',
    emptyOutDir: true,
    rollupOptions: {
      input: 'index.html' // Usar el index.html como entrada
    }
  }
});
