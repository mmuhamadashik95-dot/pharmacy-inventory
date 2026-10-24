"""pharmacy-inventory: small pharmacy stock manager with low-stock alerts
and expiry flags. JSON storage. Educational/demo only — not medical advice.
"""
import json, os, sys
from datetime import date

DEFAULT_STORE = os.path.join(os.path.dirname(__file__), "..", "inventory.json")

def load(store):
    if os.path.exists(store):
        with open(store) as f:
            return json.load(f)
    return {}

def save(store, data):
    with open(store, "w") as f:
        json.dump(data, f, indent=2)

def add_item(store, name, qty, low_at=10, expiry=None):
    data = load(store)
    data[name] = {"qty": int(qty), "low_at": int(low_at), "expiry": expiry}
    save(store, data)
    return data[name]

def stock_in(store, name, qty):
    data = load(store); data[name]["qty"] += int(qty); save(store, data); return data[name]

def stock_out(store, name, qty):
    data = load(store)
    if data[name]["qty"] < int(qty):
        raise ValueError(f"Insufficient stock for {name}: have {data[name]['qty']}, need {qty}")
    data[name]["qty"] -= int(qty); save(store, data); return data[name]

def low_stock(store):
    return {n: v for n, v in load(store).items() if v["qty"] <= v["low_at"]}

def expired(store, today=None):
    today = today or date.today().isoformat()
    return {n: v for n, v in load(store).items() if v.get("expiry") and v["expiry"] < today}

def main(argv):
    store = os.environ.get("PHARMACY_INVENTORY_STORE", DEFAULT_STORE)
    if len(argv) < 2:
        print("Usage: inventory.py add <name> <qty> [low_at] [expiry YYYY-MM-DD] | in <name> <qty> | out <name> <qty> | low | expired | list")
        return 1
    cmd = argv[1]
    if cmd == "add":
        it = add_item(store, argv[2], argv[3], argv[4] if len(argv) > 4 else 10, argv[5] if len(argv) > 5 else None)
        print(f"Added {argv[2]}: {it}")
    elif cmd == "in":
        print(stock_in(store, argv[2], argv[3]))
    elif cmd == "out":
        try:
            print(stock_out(store, argv[2], argv[3]))
        except ValueError as e:
            print("ERROR:", e); return 1
    elif cmd == "low":
        for n, v in low_stock(store).items():
            print(f"LOW {n}: {v['qty']} (threshold {v['low_at']})")
    elif cmd == "expired":
        for n, v in expired(store).items():
            print(f"EXPIRED {n}: expiry {v['expiry']}")
    elif cmd == "list":
        for n, v in load(store).items():
            print(f"{n}: qty={v['qty']} low_at={v['low_at']} expiry={v.get('expiry')}")
    else:
        print("Unknown command:", cmd); return 1
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
