#!/usr/bin/env python3
"""Atualiza catalog.json lendo pastas públicas do Google Drive."""
import json, os, re, urllib.parse, urllib.request
from pathlib import Path
KEY=os.environ.get("DRIVE_API_KEY")
if not KEY:
    raise SystemExit("DRIVE_API_KEY não configurada")
ROOT=Path(__file__).resolve().parents[1]
sources=json.loads((ROOT/"sources.json").read_text(encoding="utf-8"))
def list_folder(fid):
    files=[]; token=None
    while True:
        q={"q":f"'{fid}' in parents and trashed = false","fields":"nextPageToken,files(id,name,mimeType,modifiedTime)","pageSize":"1000","key":KEY}
        if token:q["pageToken"]=token
        url="https://www.googleapis.com/drive/v3/files?"+urllib.parse.urlencode(q)
        with urllib.request.urlopen(url,timeout=30) as r: data=json.load(r)
        files+=data.get("files",[])
        token=data.get("nextPageToken")
        if not token:break
    return files
works=[]
for source in sources["works"]:
    folders=list_folder(source["folderId"])
    chapters=[]
    for folder in folders:
        if folder["mimeType"]!="application/vnd.google-apps.folder":continue
        m=re.search(r"(?:cap[ií]tulo|cap|chapter)\s*[-_. ]*0*(\d+)",folder["name"],re.I)
        if not m:continue
        number=int(m.group(1))
        pages=[f for f in list_folder(folder["id"]) if f["mimeType"].startswith("image/")]
        def order(f):
            match=re.search(r"(\d+)(?!.*\d)",f["name"])
            return (int(match.group(1)) if match else 10**9,f["name"].casefold())
        pages.sort(key=order)
        if pages:chapters.append({"number":number,"title":"O Despertar" if source["id"]=="dragao-oculto" and number==1 else folder["name"],"pages":[f["id"] for f in pages]})
    chapters.sort(key=lambda c:c["number"],reverse=True)
    works.append({**{k:v for k,v in source.items() if k!="folderId"},"chapters":chapters})
from datetime import datetime,timezone
output={"generatedAt":datetime.now(timezone.utc).isoformat(),"works":works}
(ROOT/"catalog.json").write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("Atualizado:",[(w["title"],len(w["chapters"])) for w in works])
