#!/usr/bin/env python3
"""Check every cvar in cfg/ still exists in TF2 and is settable.

    python tools/validate-cvars.py [path/to/cvarlist.log]

Defaults to the dump committed at tools/cvarlist.log. To refresh it after a TF2
update, in the game console:

    con_logfile cvarlist.log
    cvarlist
    con_logfile ""

then copy tf/cvarlist.log over tools/cvarlist.log and commit. The diff IS the
answer to "what did this update change".

Not a test in the TDD sense -- a config has no behaviour to drive out. This
exists because a cvar TF2 has dropped prints "Unknown command" and then looks
exactly like a setting that works. Two silent failure modes:

  MISSING  the cvar no longer exists; the line does nothing
  CHEAT    sv_cheats-gated, so it cannot be set on a normal server
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DUMP = ROOT / "tools" / "cvarlist.log"
CFG = ROOT / "cfg"

# Console commands, not cvars -- nothing to look up.
NOT_CVARS = {"alias", "bind", "echo", "exec", "unbind", "unbindall", "wait"}


def load(dump):
    """Parse `name : value : flags : help` lines out of a cvarlist dump."""
    live = {}
    for line in dump.read_text(encoding="utf-8", errors="replace").splitlines():
        if ":" not in line:
            continue
        parts = [p.strip() for p in line.split(":")]
        if len(parts) >= 3 and parts[0] and " " not in parts[0]:
            live[parts[0].lower()] = parts[2]
    return live


def main():
    dump = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DUMP
    if not dump.is_file():
        raise SystemExit(f"no cvar dump at {dump} -- see the docstring for how to make one")

    live = load(dump)
    if not live:
        # Guard the instrument, not just the measurement: a dump that parses to
        # nothing would otherwise report every cvar as MISSING, which reads like
        # a catastrophic config rather than a bad file path.
        raise SystemExit(f"{dump} parsed to zero cvars; wrong file, or the format changed")

    problems, checked = [], 0
    for path in sorted(CFG.rglob("*.cfg")):
        for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            line = raw.split("//")[0].strip()
            if not line:
                continue
            token = line.split()[0]
            if token in NOT_CVARS or token.startswith(("+", "-")):
                continue
            checked += 1
            flags = live.get(token.lower())
            where = f"{path.relative_to(ROOT)}:{number}"
            if flags is None:
                problems.append(f"  {where}  MISSING  {line}")
            elif "cheat" in flags:
                problems.append(f"  {where}  CHEAT    {line}   [{flags}]")

    for problem in problems:
        print(problem)
    print(f"\nchecked {checked} cvar sets against {len(live)} live cvars from {dump.name}")
    if problems:
        raise SystemExit(f"{len(problems)} problem(s)")
    print("all present, none cheat-gated")


if __name__ == "__main__":
    main()
