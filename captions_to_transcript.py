
import json
import glob
import os
import sys

name = sys.argv[1]
files = glob.glob(f"{name}.en.json3")

if not files:
    sys.exit("No caption file found")

with open(files[0], encoding="utf-8") as f:
    data = json.load(f)

items = []

for ev in data.get("events", []):
    if "segs" not in ev:
        continue

    start = ev.get("tStartMs", 0) / 1000
    duration = ev.get("dDurationMs", 0) / 1000
    text = "".join(s.get("utf8", "") for s in ev["segs"])
    words = text.replace("\n", " ").split()

    if not words:
        continue

    word_duration = duration / len(words) if duration > 0 else 0.1

    for i, word in enumerate(words):
        items.append({
            "type": "pronunciation",
            "start_time": f"{start + i * word_duration:.2f}",
            "end_time": f"{start + (i + 1) * word_duration:.2f}",
            "alternatives": [
                {"confidence": "1.0", "content": word}
            ]
        })

os.makedirs("out", exist_ok=True)

transcript = " ".join(
    item["alternatives"][0]["content"] for item in items
)

output = {
    "jobName": name,
    "results": {
        "transcripts": [{"transcript": transcript}],
        "items": items
    }
}

with open(f"out/{name}.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"{len(items)} words written to out/{name}.json")
