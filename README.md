# Pin-Config

TF2 config, two profiles, plain `.cfg` files. No modules, no VPKs, no launcher.

```
exec low      max frames, for playing
exec ultra    max quality, for reference capture against Tf2DemoSalvage
```

Install by copying `cfg/` into `tf/cfg/`. `autoexec.cfg` holds binds, aliases,
net settings and sensitivity, and ends by exec'ing one of the two profiles.

Mouse: `sens8`, `sens10`, `sens12` switch inches-per-360 at 800 dpi. The
arithmetic is in `autoexec.cfg` so another distance or another mouse is a
calculation rather than a memory.

## Editing while TF2 is open

**TF2 caches a cfg file's contents. Overwriting one under a running client does
nothing until you `exec` it again — and the first read after an overwrite can
still serve the old copy.**

This cost an evening. A crash was traced to `mat_reducefillrate 1`, the cvar was
removed, and the game crashed again — apparently disproving the fix. It had not:
the client was still running the pre-fix file. Two rounds of diagnosis went into
a bug that was already fixed.

When testing a config change, **restart the client** rather than trusting an
`exec`. If that is too slow, type the individual cvar in console, which is read
immediately and is also a cleaner experiment.

## Checking it still works after a TF2 update

```
python tools/validate-cvars.py
```

Every cvar in `cfg/` is checked against `tools/cvarlist.log`, a dump of what the
game actually has. Two silent failure modes it catches:

- **MISSING** — the cvar is gone; TF2 prints `Unknown command` and the line looks
  exactly like a setting that works. Seven cvars from the 2014 base were dead
  this way.
- **CHEAT** — `sv_cheats`-gated, so it cannot be set on a normal server.
  `r_drawropes` is one, and mastercomfig sets it anyway.

To refresh the dump after an update, in the game console:

```
con_logfile cvarlist.log
cvarlist
con_logfile ""
```

then copy `tf/cvarlist.log` over `tools/cvarlist.log`. **The git diff is the
answer to "what did this update change".**

Note the dump truncates floats — it shows `sensitivity : 2` where the value is
2.72. It is authoritative for which cvars exist and what flags they carry, and
useless for values.

## Reading the configs

Comments after a cvar are TF2's own help text, verbatim. A `~` marks one written
by hand, because Valve ships no description for that cvar. Where a `~` line says
"undocumented", nobody knows.

`ultra.cfg` marks four settings as **PARITY** — chosen so a screenshot is
comparable against Tf2DemoSalvage's renderer rather than to look best. Mostly
`mat_hdr_level 0`, because that renderer reads the LDR lightmap lump and does not
tonemap.

## Credit

The `low.cfg` cvar selection descends from **Comanglia's config** (v1.4, 2014),
which was good at its job. Everything here has been re-verified against a modern
client; none of his commentary survives, but the choices largely do.
