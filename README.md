# pharmacy-inventory

A small pharmacy stock manager (Python CLI): add items, stock in/out, get
low-stock alerts, and flag expired stock. Data lives in `inventory.json`
(override with `PHARMACY_INVENTORY_STORE`).

> ⚠️ Educational/demo only — not medical advice. Always consult your pharmacist or doctor.

## Usage

```bash
python src/inventory.py add Paracetamol 100 10 2027-06-30
python src/inventory.py out Paracetamol 20
python src/inventory.py low
python src/inventory.py expired
python src/inventory.py list
```

## Tests

```bash
python -m unittest discover -s tests -v
```

## Author

M.Muhamad Ashik — Founder @ Prescripsy · Contact: prescripsy@prescripsy.space
