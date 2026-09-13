---
name: Offline game data layer
description: How editable local game data is loaded alongside the captured static bundle.
---

The offline app uses a server-injected JSON bootstrap so browser code can read
editable game data synchronously before the captured minified bundle evaluates.
The JSON layer is designed for overrides and additions first; the embedded
capture remains a fallback until the full historical roster is migrated.

**Why:** A static browser capture cannot synchronously import JSON during module
initialization, and removing the embedded fallback would make incomplete local
records break the roulette.

**How to apply:** Keep the JSON attribute keys aligned with the bundle's rating
keys, and preserve merge behavior when adding new player or team records.