from matching_engine import MatchingEngine
from order import Order
import pytest
import heapq
import time
import threading

# Test Valid Order
def test_valid_order(capsys):
    matching_engine = MatchingEngine("Example Symbol")
    order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=1,
                  limitprice=110.0,
                  amount=60) 
    matching_engine.handle_order(order)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] accepted order from [UUID], Direction: Bid, Limit Price: 110.0, and Amount: 60"

# Test Invalid Orders
# Price below trading range, 90.0 is outside the limit price range
def test_price_below_trading_range(capsys):
    matching_engine = MatchingEngine("Example Symbol")
    order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=1,
                  limitprice=90.0,
                  amount=50) 
    matching_engine.handle_order(order)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] rejected order from [UUID], Direction: Bid, Limit Price: 90.0, and Amount: 50, Reason: order limit price is outside the valid trading range"

# Price below trading range, 220.0 is outside the limit price range
def test_price_above_trading_range(capsys):
    matching_engine = MatchingEngine("Example Symbol")
    order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=1,
                  limitprice=220.0,
                  amount=50) 
    matching_engine.handle_order(order)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] rejected order from [UUID], Direction: Bid, Limit Price: 220.0, and Amount: 50, Reason: order limit price is outside the valid trading range"

# Amount below trading range, 0 is outside the amount range
def test_amount_below_trading_range(capsys):
    matching_engine = MatchingEngine("Example Symbol")
    order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=1,
                  limitprice=110.0,
                  amount=0) 
    matching_engine.handle_order(order)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] rejected order from [UUID], Direction: Bid, Limit Price: 110.0, and Amount: 0, Reason: order amount is outside the valid trading range"

# Amount below trading range, 111 is outside the amount range
def test_amount_above_trading_range(capsys):
    matching_engine = MatchingEngine("Example Symbol")
    order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=1,
                  limitprice=110.0,
                  amount=111) 
    matching_engine.handle_order(order)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] rejected order from [UUID], Direction: Bid, Limit Price: 110.0, and Amount: 111, Reason: order amount is outside the valid trading range"

# Testing orders get added to the list correctly
def test_single_buy_order_added_correctly():
    matching_engine = MatchingEngine("Example Symbol")
    order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=1,
                  limitprice=110.0,
                  amount=60) 
    matching_engine.handle_order(order)
    assert len(matching_engine._MatchingEngine__buy_orders) == 1
    assert matching_engine._MatchingEngine__buy_orders[0] == order

# Testing orders get added to the list correctly
def test_two_buy_orders_added_correctly_same_price():
    matching_engine = MatchingEngine("Example Symbol")
    order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=1,
                  limitprice=110.0,
                  amount=60) 
    matching_engine.handle_order(order)
    order2 = Order(trading_agent_uuid="UUID",
                symbol="Example Symbol",
                direction=1,
                limitprice=110.0,
                amount=60) 
    matching_engine.handle_order(order2)
    assert len(matching_engine._MatchingEngine__buy_orders) == 2
    assert heapq.heappop(matching_engine._MatchingEngine__buy_orders) == order
    assert heapq.heappop(matching_engine._MatchingEngine__buy_orders) == order2

# Testing orders get added to the list correctly
def test_three_buy_orders_added_correctly_same_price():
    matching_engine = MatchingEngine("Example Symbol")
    order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=1,
                  limitprice=110.0,
                  amount=60) 
    matching_engine.handle_order(order)
    order2 = Order(trading_agent_uuid="UUID",
                symbol="Example Symbol",
                direction=1,
                limitprice=110.0,
                amount=60) 
    matching_engine.handle_order(order2)
    order3 = Order(trading_agent_uuid="UUID",
                symbol="Example Symbol",
                direction=1,
                limitprice=110.0,
                amount=60) 
    matching_engine.handle_order(order3)
    assert len(matching_engine._MatchingEngine__buy_orders) == 3
    assert heapq.heappop(matching_engine._MatchingEngine__buy_orders) == order
    assert heapq.heappop(matching_engine._MatchingEngine__buy_orders) == order2
    assert heapq.heappop(matching_engine._MatchingEngine__buy_orders) == order3

# Testing orders get added to the list correctly
def test_two_buy_orders_added_correctly_different_price():
    matching_engine = MatchingEngine("Example Symbol")
    order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=1,
                  limitprice=110.0,
                  amount=60) 
    matching_engine.handle_order(order)
    order2 = Order(trading_agent_uuid="UUID",
                symbol="Example Symbol",
                direction=1,
                limitprice=150.0,
                amount=60) 
    matching_engine.handle_order(order2)
    assert len(matching_engine._MatchingEngine__buy_orders) == 2
    assert heapq.heappop(matching_engine._MatchingEngine__buy_orders) == order2
    assert heapq.heappop(matching_engine._MatchingEngine__buy_orders) == order

# Testing orders get added to the list correctly
def test_three_buy_orders_added_correctly_different_price():
    matching_engine = MatchingEngine("Example Symbol")
    order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=1,
                  limitprice=110.0,
                  amount=60) 
    matching_engine.handle_order(order)
    order2 = Order(trading_agent_uuid="UUID",
                symbol="Example Symbol",
                direction=1,
                limitprice=150.0,
                amount=60) 
    matching_engine.handle_order(order2)
    order3 = Order(trading_agent_uuid="UUID",
            symbol="Example Symbol",
            direction=1,
            limitprice=130.0,
            amount=60) 
    matching_engine.handle_order(order3)
    assert len(matching_engine._MatchingEngine__buy_orders) == 3
    assert heapq.heappop(matching_engine._MatchingEngine__buy_orders) == order2
    assert heapq.heappop(matching_engine._MatchingEngine__buy_orders) == order3
    assert heapq.heappop(matching_engine._MatchingEngine__buy_orders) == order

# Testing orders get added to the list correctly
def test_single_sell_order_added_correctly():
    matching_engine = MatchingEngine("Example Symbol")
    order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=0,
                  limitprice=110.0,
                  amount=60) 
    matching_engine.handle_order(order)
    assert len(matching_engine._MatchingEngine__sell_orders) == 1
    assert matching_engine._MatchingEngine__sell_orders[0] == order

# Testing orders get added to the list correctly
def test_two_sell_orders_added_correctly_same_price():
    matching_engine = MatchingEngine("Example Symbol")
    order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=0,
                  limitprice=110.0,
                  amount=60) 
    matching_engine.handle_order(order)
    order2 = Order(trading_agent_uuid="UUID",
                symbol="Example Symbol",
                direction=0,
                limitprice=110.0,
                amount=60) 
    matching_engine.handle_order(order2)
    assert len(matching_engine._MatchingEngine__sell_orders) == 2
    assert heapq.heappop(matching_engine._MatchingEngine__sell_orders) == order
    assert heapq.heappop(matching_engine._MatchingEngine__sell_orders) == order2

# Testing orders get added to the list correctly
def test_three_sell_orders_added_correctly_same_price():
    matching_engine = MatchingEngine("Example Symbol")
    order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=0,
                  limitprice=110.0,
                  amount=60) 
    matching_engine.handle_order(order)
    order2 = Order(trading_agent_uuid="UUID",
                symbol="Example Symbol",
                direction=0,
                limitprice=110.0,
                amount=60) 
    matching_engine.handle_order(order2)
    order3 = Order(trading_agent_uuid="UUID",
                symbol="Example Symbol",
                direction=0,
                limitprice=110.0,
                amount=60) 
    matching_engine.handle_order(order3)
    assert len(matching_engine._MatchingEngine__sell_orders) == 3
    assert heapq.heappop(matching_engine._MatchingEngine__sell_orders) == order
    assert heapq.heappop(matching_engine._MatchingEngine__sell_orders) == order2
    assert heapq.heappop(matching_engine._MatchingEngine__sell_orders) == order3

# Testing orders get added to the list correctly
def test_two_sell_orders_added_correctly_different_price():
    matching_engine = MatchingEngine("Example Symbol")
    order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=0,
                  limitprice=110.0,
                  amount=60) 
    matching_engine.handle_order(order)
    order2 = Order(trading_agent_uuid="UUID",
                symbol="Example Symbol",
                direction=0,
                limitprice=150.0,
                amount=60) 
    matching_engine.handle_order(order2)
    assert len(matching_engine._MatchingEngine__sell_orders) == 2
    assert heapq.heappop(matching_engine._MatchingEngine__sell_orders) == order
    assert heapq.heappop(matching_engine._MatchingEngine__sell_orders) == order2

# Testing orders get added to the list correctly
def test_three_sell_orders_added_correctly_different_price():
    matching_engine = MatchingEngine("Example Symbol")
    order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=0,
                  limitprice=110.0,
                  amount=60) 
    matching_engine.handle_order(order)
    order2 = Order(trading_agent_uuid="UUID",
                symbol="Example Symbol",
                direction=0,
                limitprice=150.0,
                amount=60) 
    matching_engine.handle_order(order2)
    order3 = Order(trading_agent_uuid="UUID",
            symbol="Example Symbol",
            direction=0,
            limitprice=130.0,
            amount=60) 
    matching_engine.handle_order(order3)
    assert len(matching_engine._MatchingEngine__sell_orders) == 3
    assert heapq.heappop(matching_engine._MatchingEngine__sell_orders) == order
    assert heapq.heappop(matching_engine._MatchingEngine__sell_orders) == order3
    assert heapq.heappop(matching_engine._MatchingEngine__sell_orders) == order2

# Testing jobs are removed after 5 seconds
def scheduler(matching_engine):
    time_to_run = 10
    start_time = time.time()
    while time.time() - start_time < time_to_run:
        matching_engine._MatchingEngine__scheduler.exec_jobs()

def test_order_removed_ttl(capsys):
    matching_engine = MatchingEngine("Example Symbol")
    order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=0,
                  limitprice=110.0,
                  amount=60)
    thread = threading.Thread(target=scheduler, args=(matching_engine,))
    thread.start() 
    matching_engine.handle_order(order)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] accepted order from [UUID], Direction: Offer, Limit Price: 110.0, and Amount: 60"
    assert len(matching_engine._MatchingEngine__sell_orders) == 1
    assert matching_engine._MatchingEngine__sell_orders[0] == order
    # After 6 seconds the jobs should have been removed
    time.sleep(6)
    assert len(matching_engine._MatchingEngine__sell_orders) == 0
    thread.join()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] rejected order from [UUID], Direction: Offer, Limit Price: 110.0, and Amount: 60, Reason: order timeout"

# Testing that the trade matching is working
def test_trade_matching_valid_buy_and_sell_same_price_same_amount(capsys):
    matching_engine = MatchingEngine("Example Symbol")
    sell_order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=0,
                  limitprice=110.0,
                  amount=60)
    matching_engine.handle_order(sell_order)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] accepted order from [UUID], Direction: Offer, Limit Price: 110.0, and Amount: 60"
    assert len(matching_engine._MatchingEngine__sell_orders) == 1
    assert matching_engine._MatchingEngine__sell_orders[0] == sell_order
    buy_order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=1,
                  limitprice=110.0,
                  amount=60)
    matching_engine.handle_order(buy_order)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] accepted order from [UUID], Direction: Bid, Limit Price: 110.0, and Amount: 60"
    assert len(matching_engine._MatchingEngine__buy_orders) == 1
    assert matching_engine._MatchingEngine__buy_orders[0] == buy_order
    matching_engine.match_orders()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] accepted buy order from [UUID] for a unit price of 110.0 for 60 units from [UUID]"
    assert len(matching_engine._MatchingEngine__sell_orders) == 0
    assert len(matching_engine._MatchingEngine__buy_orders) == 0

# Testing that the trade matching is working
def test_trade_matching_valid_buy_and_sell_same_price_sell_lower_amount(capsys):
    matching_engine = MatchingEngine("Example Symbol")
    sell_order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=0,
                  limitprice=110.0,
                  amount=40)
    matching_engine.handle_order(sell_order)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] accepted order from [UUID], Direction: Offer, Limit Price: 110.0, and Amount: 40"
    assert len(matching_engine._MatchingEngine__sell_orders) == 1
    assert matching_engine._MatchingEngine__sell_orders[0] == sell_order
    buy_order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=1,
                  limitprice=110.0,
                  amount=60)
    matching_engine.handle_order(buy_order)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] accepted order from [UUID], Direction: Bid, Limit Price: 110.0, and Amount: 60"
    assert len(matching_engine._MatchingEngine__buy_orders) == 1
    assert matching_engine._MatchingEngine__buy_orders[0] == buy_order
    matching_engine.match_orders()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] accepted buy order from [UUID] for a unit price of 110.0 for 40 units from [UUID]"
    assert len(matching_engine._MatchingEngine__sell_orders) == 0
    assert len(matching_engine._MatchingEngine__buy_orders) == 1
    assert matching_engine._MatchingEngine__buy_orders[0].amount == 20

# Testing that the trade matching is working
def test_trade_matching_valid_buy_and_sell_same_price_sell_higher_amount(capsys):
    matching_engine = MatchingEngine("Example Symbol")
    sell_order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=0,
                  limitprice=110.0,
                  amount=80)
    matching_engine.handle_order(sell_order)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] accepted order from [UUID], Direction: Offer, Limit Price: 110.0, and Amount: 80"
    assert len(matching_engine._MatchingEngine__sell_orders) == 1
    assert matching_engine._MatchingEngine__sell_orders[0] == sell_order
    buy_order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=1,
                  limitprice=110.0,
                  amount=60)
    matching_engine.handle_order(buy_order)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] accepted order from [UUID], Direction: Bid, Limit Price: 110.0, and Amount: 60"
    assert len(matching_engine._MatchingEngine__buy_orders) == 1
    assert matching_engine._MatchingEngine__buy_orders[0] == buy_order
    matching_engine.match_orders()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] accepted buy order from [UUID] for a unit price of 110.0 for 60 units from [UUID]"
    assert len(matching_engine._MatchingEngine__sell_orders) == 1
    assert matching_engine._MatchingEngine__sell_orders[0].amount == 20
    assert len(matching_engine._MatchingEngine__buy_orders) == 0

# Testing that the trade matching is working
def test_trade_matching_valid_buy_and_sell_lower_price_sell_same_amount(capsys):
    matching_engine = MatchingEngine("Example Symbol")
    sell_order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=0,
                  limitprice=105.0,
                  amount=60)
    matching_engine.handle_order(sell_order)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] accepted order from [UUID], Direction: Offer, Limit Price: 105.0, and Amount: 60"
    assert len(matching_engine._MatchingEngine__sell_orders) == 1
    assert matching_engine._MatchingEngine__sell_orders[0] == sell_order
    buy_order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=1,
                  limitprice=110.0,
                  amount=60)
    matching_engine.handle_order(buy_order)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] accepted order from [UUID], Direction: Bid, Limit Price: 110.0, and Amount: 60"
    assert len(matching_engine._MatchingEngine__buy_orders) == 1
    assert matching_engine._MatchingEngine__buy_orders[0] == buy_order
    matching_engine.match_orders()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] accepted buy order from [UUID] for a unit price of 105.0 for 60 units from [UUID]"
    assert len(matching_engine._MatchingEngine__sell_orders) == 0
    assert len(matching_engine._MatchingEngine__buy_orders) == 0

# Testing that the trade matching is working
def test_trade_matching_valid_buy_and_sell_higher_price_sell_same_amount(capsys):
    matching_engine = MatchingEngine("Example Symbol")
    sell_order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=0,
                  limitprice=115.0,
                  amount=60)
    matching_engine.handle_order(sell_order)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] accepted order from [UUID], Direction: Offer, Limit Price: 115.0, and Amount: 60"
    assert len(matching_engine._MatchingEngine__sell_orders) == 1
    assert matching_engine._MatchingEngine__sell_orders[0] == sell_order
    buy_order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=1,
                  limitprice=110.0,
                  amount=60)
    matching_engine.handle_order(buy_order)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] accepted order from [UUID], Direction: Bid, Limit Price: 110.0, and Amount: 60"
    assert len(matching_engine._MatchingEngine__buy_orders) == 1
    assert matching_engine._MatchingEngine__buy_orders[0] == buy_order
    matching_engine.match_orders()
    assert len(matching_engine._MatchingEngine__sell_orders) == 1
    assert len(matching_engine._MatchingEngine__buy_orders) == 1
    assert matching_engine._MatchingEngine__sell_orders[0] == sell_order
    assert matching_engine._MatchingEngine__buy_orders[0] == buy_order

# Testing that the trade matching is working
def test_trade_matching_valid_buy_and_sell_two_sells_below_buy(capsys):
    matching_engine = MatchingEngine("Example Symbol")
    sell_order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=0,
                  limitprice=100.0,
                  amount=40)
    matching_engine.handle_order(sell_order)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] accepted order from [UUID], Direction: Offer, Limit Price: 100.0, and Amount: 40"
    sell_order2 = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=0,
                  limitprice=105.0,
                  amount=20)
    matching_engine.handle_order(sell_order2)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] accepted order from [UUID], Direction: Offer, Limit Price: 105.0, and Amount: 20"
    assert len(matching_engine._MatchingEngine__sell_orders) == 2
    assert matching_engine._MatchingEngine__sell_orders[0] == sell_order
    buy_order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=1,
                  limitprice=110.0,
                  amount=60)
    matching_engine.handle_order(buy_order)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] accepted order from [UUID], Direction: Bid, Limit Price: 110.0, and Amount: 60"
    assert len(matching_engine._MatchingEngine__buy_orders) == 1
    assert matching_engine._MatchingEngine__buy_orders[0] == buy_order
    matching_engine.match_orders()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] accepted buy order from [UUID] for a unit price of 100.0 for 40 units from [UUID]"
    matching_engine.match_orders()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] accepted buy order from [UUID] for a unit price of 105.0 for 20 units from [UUID]"
    assert len(matching_engine._MatchingEngine__sell_orders) == 0
    assert len(matching_engine._MatchingEngine__buy_orders) == 0

# Testing that the trade matching is working
def test_trade_matching_valid_buy_and_sell_two_sells_one_above_one_below(capsys):
    matching_engine = MatchingEngine("Example Symbol")
    sell_order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=0,
                  limitprice=100.0,
                  amount=40)
    matching_engine.handle_order(sell_order)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] accepted order from [UUID], Direction: Offer, Limit Price: 100.0, and Amount: 40"
    sell_order2 = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=0,
                  limitprice=115.0,
                  amount=20)
    matching_engine.handle_order(sell_order2)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] accepted order from [UUID], Direction: Offer, Limit Price: 115.0, and Amount: 20"
    assert len(matching_engine._MatchingEngine__sell_orders) == 2
    assert matching_engine._MatchingEngine__sell_orders[0] == sell_order
    buy_order = Order(trading_agent_uuid="UUID",
                  symbol="Example Symbol",
                  direction=1,
                  limitprice=110.0,
                  amount=60)
    matching_engine.handle_order(buy_order)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] accepted order from [UUID], Direction: Bid, Limit Price: 110.0, and Amount: 60"
    assert len(matching_engine._MatchingEngine__buy_orders) == 1
    assert matching_engine._MatchingEngine__buy_orders[0] == buy_order
    matching_engine.match_orders()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Matching Engine with Symbol [Example Symbol] accepted buy order from [UUID] for a unit price of 100.0 for 40 units from [UUID]"
    matching_engine.match_orders()
    assert len(matching_engine._MatchingEngine__sell_orders) == 1
    assert len(matching_engine._MatchingEngine__buy_orders) == 1
    assert matching_engine._MatchingEngine__buy_orders[0].amount == 20