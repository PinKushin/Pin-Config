import pathlib, sys
TF=pathlib.Path("F:/SteamLibrary/steamapps/common/Team Fortress 2/tf")
CFG=pathlib.Path("C:/Users/pinku/source/repos/PinKushin/Pin-Config/cfg")
live={}
for line in (TF/"cvarlist.log").read_text(encoding="utf-8",errors="replace").splitlines():
    if ":" in line:
        p=[x.strip() for x in line.split(":")]
        if len(p)>=3 and p[0] and " " not in p[0]: live[p[0].lower()]=p[2]
SKIP={"alias","bind","echo","exec","unbind","wait","unbindall"}
bad=cheat=total=0
for f in sorted(CFG.glob("*.cfg")):
    problems=[]
    for n,raw in enumerate(f.read_text(encoding="utf-8").splitlines(),1):
        line=raw.split("//")[0].strip()
        if not line: continue
        tok=line.split()[0]
        if tok in SKIP or tok.startswith(("+","-")): continue
        total+=1
        flags=live.get(tok.lower())
        if flags is None: problems.append(f"  {f.name}:{n}  MISSING   {line}"); bad+=1
        elif "cheat" in flags: problems.append(f"  {f.name}:{n}  CHEAT     {line}   [{flags}]"); cheat+=1
    for p in problems: print(p)
print(f"\nchecked {total} cvar sets across {len(list(CFG.glob('*.cfg')))} files")
print(f"  missing from TF2: {bad}")
print(f"  cheat-flagged:    {cheat}")
sys.exit(1 if (bad or cheat) else 0)
