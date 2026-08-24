# 🚐 Van Itinerary Builder

Paved-road itinerary planner for van/SUV overlanding across **North & Central America**.
Enter an origin, destination, and any intermediate stops; get a map route, colorblind-safe
daily stages (capped by drive time *and* optional climb), an altitude profile, campgrounds,
a safety-advisory check, and a written explanation of *why* the route was chosen.

## Map provider: OpenStreetMap, not Google — and why

For this specific app the OpenStreetMap stack (Leaflet + OpenRouteService + Overpass) is
clearly more effective than Google Maps Platform:

| Need | OpenStreetMap stack | Google Maps Platform |
|---|---|---|
| Van / heavy-vehicle routing | ✅ `driving-hgv` profile | ❌ no truck/van profile in the public Directions API |
| "Paved only" | ✅ OSM `surface` tags + HGV weighting | ❌ no avoid-unpaved option |
| Elevation along the route | ✅ 3D geometry returned inline (SRTM) | ⚠️ separate paid Elevation API calls |
| Free POI / campground queries | ✅ Overpass (unlimited, no key) | ❌ Places billed per request |
| Cost & terms | ✅ free, open data (ODbL), self-hostable, results cacheable | ❌ billing required; TOS restricts storing/derivative use |
| Where Google wins | — | live traffic, richer place metadata, geocoding polish |

Google would only pull ahead if live traffic and place reviews were the priority. For a
van-profiled, paved-only, elevation-aware overland planner, OSM wins on every core axis, so
the app is built on it.

## Daily-stage colors

Stages use the **Okabe–Ito** colorblind-safe qualitative palette (safe for deuteranopia,
protanopia, and tritanopia), ordered so consecutive days stay maximally distinct.

## Run it

```bash
cd ca-van-router
python3 -m http.server 8777
# open http://localhost:8777/index.html
```

Or just open `index.html` in a browser.

## One-time setup: routing key

Routing uses **OpenRouteService** (free, 2,000 routes/day).
1. Sign up: https://openrouteservice.org/dev/#/signup
2. Copy your API token.
3. Paste it into the app's "One-time setup" box → **Save key**. It's stored only in your browser (localStorage).

## What it does & how

| Requirement | How it's met | Honest limits |
|---|---|---|
| Van, real roads | ORS `driving-hgv` (heavy-vehicle) profile → favors highways wide enough for a van | — |
| Paved only | HGV profile + OSM surface weighting de-prioritizes tracks | No engine guarantees 100% paved; verify final dirt access to campsites |
| Safe areas | Route checked against a **curated advisory layer** (`ADVISORIES` in `index.html`) built from public travel notices + overlander reports | **Not a live feed.** Always cross-check State Dept / FCDO / iOverlander |
| Max 4–5 h/day | Route split into daily stages by cumulative drive time (toggle 4 / 4.5 / 5 h) | Overnight points are approximate — nudge to nearest town |
| ≤ 1000 m climb/day | Optional pill; a day is also cut when cumulative ascent hits 1000 m (climb-capped days are flagged) | Uses SRTM elevation along the route |
| Multi-stop trips | Add any number of intermediate stops (**+ Add stop**); routes through all of them in order | — |
| Reorder stops | **▲ / ▼** buttons on each stop row reorder the sequence before planning | — |
| Tourist attractions | **Selectable source** dropdown: **GeoNames** (offline bundled DB, 12,115 sites for GT/MX/US — instant, default), **Wikipedia** (geosearch, article links, global), or **OpenStreetMap** (typed POIs, global). Switching the source re-runs attractions without re-planning | GeoNames covers only GT/MX/US; Wikipedia/OSM are global. All pins link to Google Maps + Wikipedia when available; capped at 120 |
| GeoNames attractions data | `attractions_geonames.js` — extracted from GeoNames country dumps, filtered to visitor feature codes (archaeological sites, volcanoes, museums, waterfalls, historic sites, caves, beaches…); churches/parks/utility-towers excluded | GT 442 · MX 1,812 · US 9,861. Regenerate from `GeoNames/<CC>/<CC>.txt` |
| POI icons & descriptions | Each attraction pin uses a **kind-specific emoji icon** (🌋 volcano, 🏛️ museum, 💧 waterfall, 🏖️ beach, 🏰 castle…) and its popup shows a **short description** — the real Wikidata one-liner for Wikipedia POIs, a canned blurb otherwise | — |
| Startup | The page opens with a **clean itinerary** (two empty stops) | Use a saved itinerary's ↺ to reload a previous one |
| Mobile | On screens ≤ 820px a **📋 Plan / 🗺️ Map toggle bar** appears: each view is full-screen; planning auto-switches to the Map. Desktop is unchanged (side-by-side) | Leaflet `invalidateSize()` + re-fit on switch so tiles/route render correctly |
| Planet Fitness | Optional 🏋️ pill — **Planet Fitness branches within 25 km** of the route (showers / 24h access), pins with a Google Maps search link. Data © [SimpleMaps](https://simplemaps.com/data/business/planet-fitness), `gyms_planet_fitness.js` (2,730 US locations) | "Platen Fitness" isn't a real chain — this is Planet Fitness; SimpleMaps set is US |
| National & State parks | Optional 🏞️ pill — **national (🏞️) and state (🌲) parks within 40 km** of the route, from GeoNames (`parks.js`, 2,880 across GT/MX/US), pins with a Google Maps search link | Name-matched from GeoNames dumps |
| Route comparison | Separate **⚖️ Compare routes (A→B)** section: builds up to **3 distinct paths** (direct + perpendicular-offset vias, since ORS `alternative_routes` caps at 100 km), scores each on **distance, driving time, pavement % (ORS surface data), safety (advisory zones), and climb**, ranks them with a weighted **points system** (safety 30 · pavement 25 · time 20 · distance 15 · climb 10), highlights the winner, draws all three on the map in colorblind-safe colors, and **suggests sources** (iOverlander/Street View/satellite for pavement; State Dept/FCDO for safety) where data is missing | Some corridors (e.g. the Central-American isthmus) genuinely have only 1–2 distinct paved routes; it says so honestly |
| City autocomplete | `cities.js` — all North + Central America cities with **population ≥ 100,000** (625, from GeoNames), merged with curated overlander towns, in the stops dropdown | Regenerate `cities.js` to change the threshold or region |
| Save / retrieve itineraries | Name and save a planned itinerary to `localStorage`; reload (↺) repopulates the form and re-plans, or delete (✕) | Stored per-browser, not synced |
| Compare itineraries | Select 2–3 saved itineraries → side-by-side table (distance, time, days, climb, max altitude, advisories) with best-per-metric highlighted + overlaid colorblind-safe elevation profiles | — |
| US campgrounds | **NPS Data API** (`developer.nps.gov`) — national-park campgrounds, per the ParkPal writeup. Needs a free NPS key | Covers NPS units, not private/BLM/state parks |
| Central-America campgrounds | Live **Overpass / OpenStreetMap** near each overnight point — no key. Covers `camp_site`, `caravan_site`, `camp_pitch`, `wilderness_hut`, `alpine_hut` (nodes + areas) | OSM coverage is patchy in rural areas. (iOverlander's own API is login-gated + CORS-blocked, so it can't be called client-side.) |
| Mexico + Guatemala campgrounds | Bundled **iOverlander dataset** (`camps_mx_gt.js`) — established campgrounds with description/facilities in the pin popups | Some records had no coords in the source; recovered via Photon geocoder (GT/MX-filtered). Regenerate with `geocode_camps.py` |
| Camp search radius | **Escalating** per overnight point: 25 km first, then 50, then 100 — returns the nearest cluster and plots only those, so the map stays uncluttered | Remote stops fall back to 100 km |
| Camp links | Each camp pin popup has a **Find on Google Maps** link that *searches by name + city + country* (not raw coordinates, which can be approximate for recovered camps), plus a Details link for NPS camps | City comes from reverse-geocoding (Photon) in `camps_mx_gt.js` |
| Colorblind-safe stages | Okabe–Ito palette for day colors on map, chart, and stage cards | — |
| Origin/destination input | Geocoded within a North + Central America bounding box | Add the country name if a place is ambiguous |
| Altitude visualization | 3D route geometry (SRTM elevation) → SVG profile + total gain/loss + high-pass warning | — |
| Explain the route | "Why this route?" panel summarizes profile, paving, terrain, stages, advisories | — |

## Extending the "public data" layer

The safety/advisory data is the curated `ADVISORIES` array near the top of the
`<script>` in `index.html`. Each entry is:

```js
{name, lat, lon, radiusKm, level: "warn" | "danger", note}
```

Add border-crossing tips, crime hotspots, or authority notices as you gather them.
The app draws each as a circle on the map and flags it when your route passes within its radius.

## Data & credits
Routing © OpenRouteService · map & surface data © OpenStreetMap contributors · elevation from SRTM.
