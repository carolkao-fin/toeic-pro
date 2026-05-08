"""
從 Hugging Face 資料集 kknono668/toeic-vocab-tw 下載 TOEIC 詞彙
授權：CC-BY-SA-4.0
目標分數 850+，篩選 600-780、780-900、900+ 三個區間
"""
import json
import urllib.request
import urllib.parse

BASE = "https://datasets-server.huggingface.co/rows"
DATASET = "kknono668/toeic-vocab-tw"
TARGET_RANGES = {"600-780", "780-900", "900+"}
# 每次最多 100 筆，預計 11200 筆 → 最多 112 次，但我們只要符合條件的
BATCH = 100
MAX_ROWS = 5000   # 先抓前 5000 筆，從中篩選

def fetch_batch(offset, length=100):
    params = urllib.parse.urlencode({
        "dataset": DATASET,
        "config": "default",
        "split": "train",
        "offset": offset,
        "length": length,
    })
    url = f"{BASE}?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def main():
    result = []
    offset = 0
    print("開始下載 TOEIC 詞彙資料集...")
    while offset < MAX_ROWS:
        try:
            data = fetch_batch(offset, BATCH)
        except Exception as e:
            print(f"  offset={offset} 失敗：{e}")
            break
        rows = data.get("rows", [])
        if not rows:
            break
        for item in rows:
            row = item.get("row", {})
            score_range = row.get("toeic_score_range", "")
            if score_range not in TARGET_RANGES:
                continue
            # 取第一個例句（可能是 dict 或 str）
            examples = row.get("examples", []) or []
            ex_en, ex_zh = "", ""
            if examples:
                first = examples[0]
                if isinstance(first, dict):
                    ex_en = first.get("en", first.get("english", ""))
                    ex_zh = first.get("zh", first.get("chinese", ""))
                elif isinstance(first, str):
                    ex_en = first
                    ex_zh = examples[1] if len(examples) > 1 else ""
            # 詞性
            pos_list = row.get("parts_of_speech", []) or []
            pos = pos_list[0] if pos_list else "n."
            result.append({
                "word": row.get("english_word", "").strip(),
                "pos": pos,
                "cat": row.get("category", "商務辦公"),
                "zh": row.get("chinese_definition", "").strip(),
                "ex": ex_en.strip(),
                "ex_zh": ex_zh.strip(),
                "range": score_range,
            })
        filtered = len(result)
        offset += BATCH
        print(f"  已處理 {offset} 筆，符合條件：{filtered} 筆")
        if len(rows) < BATCH:
            break

    # 去除空 word
    result = [r for r in result if r["word"] and len(r["word"]) < 50]
    # 依分數區間排序（優先 780-900）
    order = {"780-900": 0, "600-780": 1, "900+": 2}
    result.sort(key=lambda x: order.get(x["range"], 3))

    out_path = "vocab_data.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n完成！共 {len(result)} 筆，已儲存至 {out_path}")
    # 顯示前幾筆預覽
    for r in result[:5]:
        print(f"  [{r['range']}] {r['word']} ({r['pos']}) = {r['zh']}")

if __name__ == "__main__":
    main()
