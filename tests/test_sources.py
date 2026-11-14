"""当前来源接口的核心和错误路径。"""
import unittest,tempfile
from pathlib import Path
from common import read,Releases,money,digest

class CommonTests(unittest.TestCase):
    def test_snapshot_and_corruption(self):
        with tempfile.TemporaryDirectory() as d:
            store=Releases(d);raw={'value':'20.10'};key=store.publish(raw)
            self.assertEqual(store.open(key),raw);self.assertEqual(store.publish(raw),key)
            Path(d,key).write_bytes(b'changed')
            with self.assertRaises(ValueError):store.open(key)
    def test_exact_money(self):
        self.assertEqual(str(money('0.1')+money('0.2')),'0.3')
        with self.assertRaises(ValueError):money(float('nan'))

from orders import balances
from calls import cost_rows
class DomainTests(unittest.TestCase):
    def test_known_time_and_cost(self):
        d=read();self.assertEqual(balances(d,5)['o1']['paid'],100)
        self.assertEqual(balances(d,12)['o1']['paid'],70)
        self.assertEqual(cost_rows(d,12)[0]['low'],'0.40')
    def test_overuse_and_conflict(self):
        d=read();d['events'][-1]['tokens']=1000
        with self.assertRaises(ValueError):balances(d,12)
        d=read();d['events'].append(dict(d['events'][0],tokens=101))
        with self.assertRaises(ValueError):balances(d,12)
