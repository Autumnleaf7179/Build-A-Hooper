# Offline game database

`database.json` is loaded by `offline_server.py` and made available to the
browser before the captured game bundle starts. It is the editable data layer
for new attributes, player-stat overrides, and additional team records.

Player records use the player's stable `id` and an `attributes` object. The
server merges those values into the imported player-season records. Team
records can be added under `teams.franchises` and `teams.teamSeasons`; records
with an existing ID override the captured record, while new complete records
are added to the roulette pool.

The original downloaded data remains as a compatibility fallback so the
offline game still has its full historical pool when this file only contains
overrides.