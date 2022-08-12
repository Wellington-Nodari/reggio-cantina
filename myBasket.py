import unittest
import psycopg2
import psycopg2.extras
from app import items_list


conn = psycopg2.connect(dbname = "decidsulj18q74", user = "fphmyvegucmiih", password = "08bdb827e02af0eae42038539b24ecbb0bede1a077e2b210c57c326d77b5aa61", host = "ec2-3-248-121-12.eu-west-1.compute.amazonaws.com")

class Basket:
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT item_name, item_price FROM menu;")
    price = cur.fetchall()

    prices = {}
    for x in price:
        prices[x[0]] = price[0][1]

    print(prices)

    def __init__(self):
        self.__contents = {}

    def add(self, item, qty):
        if qty < 0:
            raise ValueError("Quantity cannot be negative!")
        if item not in Basket.prices:
            raise ValueError("Item not found!")
        self.__contents[item] = qty + self.__contents.get(item, 0)

    def getQuantity(self, item):
        return self.__contents.get(item, 0)

    def value(self):
        total = 0
        for i in self.__contents:
            total += self.__contents[i] * Basket.prices[i]
        return total



class TestBasket(unittest.TestCase):
    def testAdd(self):
        b = Basket()
        b.value()
        self.assertEqual(0, b.value())

    def testValue(self):
        b = Basket()
        b.add('Swordfish alla Calabrese', 2)
        b.value()
        self.assertEqual(25.9*2, b.value())

    def testAddMore(self):
        b = Basket()
        b.add('Swordfish alla Calabrese', 2)
        b.add('Swordfish alla Calabrese', 2)
        self.assertEqual(51.8*2, b.value())

    def testQtyProd(self):
        b = Basket()
        with self.assertRaises(ValueError):
            b.add('Swordfish alla Calabrese', -1)

    def testExistProd(self):
        b = Basket()
        with self.assertRaises(ValueError):
            b.add('cheese', 2)

unittest.main(argv=['ignored'],exit=False)