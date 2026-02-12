import unittest
import datetime
from solution import monthly_charge

users = [
  {
    'id': 1,
    'name': 'Employee #1',
    'activated_on': datetime.date(2019, 1, 1),
    'deactivated_on': None,
    'customer_id': 1,
  },
  {
    'id': 2,
    'name': 'Employee #2',
    'activated_on': datetime.date(2019, 1, 1),
    'deactivated_on': None,
    'customer_id': 1,
  },
]

plan = {
  'id': 1,
  'customer_id': 1,
  'monthly_price_in_cents': 5_000
}

no_users = []

# Note: the class must be called Test
class Test(unittest.TestCase):
  def test_works_when_no_users_are_active(self):
    self.assertEqual(monthly_charge('2018-10', plan, users), 0)

  def test_works_when_the_active_users_are_active_the_entire_month(self):
    expected_user_count = 2
    self.assertAlmostEqual(monthly_charge('2020-12', plan, users), expected_user_count * 5_000, delta=1)
