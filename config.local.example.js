/* ---------------------------------------------------------------------------
 * OPTIONAL local key file — pre-fills API keys so YOUR OWN machines never prompt.
 *
 * HOW TO USE:
 *   1. Copy this file to  config.local.js  (same folder as index.html).
 *   2. Put your real keys below.
 *   3. Done — index.html loads it automatically.
 *
 * ⚠️  SECURITY: config.local.js is git-ignored on purpose. NEVER commit it and
 *     NEVER put real keys on a PUBLIC site (GitHub Pages, etc.) — a client-side
 *     app exposes them to everyone. Use this only on machines you control
 *     (your laptop, your Home Assistant). Public visitors enter their own key.
 * ------------------------------------------------------------------------- */
window.VAN_KEYS = {
  ors: "PASTE_YOUR_OPENROUTESERVICE_KEY_HERE",  // required — https://openrouteservice.org/dev
  nps: ""                                       // optional — US national-park campgrounds
};
