import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/../')
import jsonActions
import json

from decimal import Decimal
from datetime import datetime, date

def test_json_convert():
    example = {
        'decimal':Decimal('2.2'),
    }
    example = jsonActions.jsonOut(example)
    json.loads(example)

def test_json_convert_2():
    example = {
        'here':[datetime.now(), date.today()]
    }
    example = jsonActions.jsonOut(example)
    json.loads(example)

def test_valid_json():
    example = {'hello':Decimal('12.2')}
    assert not jsonActions.jsonValid(example)

def test_valid_json_2():
    example = {'hello':2}
    assert jsonActions.jsonValid(example)

def test_valid_json_3():
    example = {
        'num':Decimal('23123.231')
    }
    assert jsonActions.jsonValid(jsonActions.jsonOut(example))
