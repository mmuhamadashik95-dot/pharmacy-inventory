import os, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from inventory import add_item, stock_in, stock_out, low_stock, expired

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.store = os.path.join(tempfile.mkdtemp(), "inv.json")
    def test_add_and_out(self):
        add_item(self.store, "Paracetamol", 100)
        stock_out(self.store, "Paracetamol", 30)
        self.assertEqual(low_stock(self.store), {})
        stock_out(self.store, "Paracetamol", 65)
        self.assertIn("Paracetamol", low_stock(self.store))
    def test_overdraw_rejected(self):
        add_item(self.store, "Aspirin", 5)
        with self.assertRaises(ValueError):
            stock_out(self.store, "Aspirin", 10)
    def test_stock_in(self):
        add_item(self.store, "Cetirizine", 2, low_at=5)
        stock_in(self.store, "Cetirizine", 10)
        self.assertNotIn("Cetirizine", low_stock(self.store))
    def test_expired(self):
        add_item(self.store, "Old Syrup", 3, expiry="2020-01-01")
        add_item(self.store, "Fresh Tab", 3, expiry="2999-01-01")
        self.assertIn("Old Syrup", expired(self.store))
        self.assertNotIn("Fresh Tab", expired(self.store))

if __name__ == "__main__":
    unittest.main()
