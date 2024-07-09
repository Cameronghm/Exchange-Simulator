from order import Order
import heapq
import time
import datetime as dt
from scheduler import Scheduler

class MatchingEngine:
    def __init__(self, symbol):
        self.symbol = symbol
        self.__buy_orders = []
        self.__sell_orders = []
        self.__scheduler = Scheduler(n_threads=0)

    def run(self):
        while True:
            self.__scheduler.exec_jobs()
            self.match_orders()

    def match_orders(self):
        if len(self.__sell_orders) > 0 and len(self.__buy_orders) > 0:
            priority_sell_order = self.__sell_orders[0]
            priority_buy_order = self.__buy_orders[0]
            if priority_sell_order.limitprice <= priority_buy_order.limitprice:
                if priority_sell_order.amount < priority_buy_order.amount:
                    print(f"Matching Engine with Symbol [{self.symbol}] accepted buy order from [{priority_buy_order.originator}] for a unit price of {str(priority_sell_order.limitprice)} for {str(priority_sell_order.amount)} units from [{priority_sell_order.originator}]")
                    priority_buy_order.amount -= priority_sell_order.amount
                    _ = heapq.heappop(self.__sell_orders)
                elif priority_sell_order.amount == priority_buy_order.amount:
                    print(f"Matching Engine with Symbol [{self.symbol}] accepted buy order from [{priority_buy_order.originator}] for a unit price of {str(priority_sell_order.limitprice)} for {str(priority_buy_order.amount)} units from [{priority_sell_order.originator}]")
                    _ = heapq.heappop(self.__buy_orders)
                    _ = heapq.heappop(self.__sell_orders)
                else:
                    print(f"Matching Engine with Symbol [{self.symbol}] accepted buy order from [{priority_buy_order.originator}] for a unit price of {str(priority_sell_order.limitprice)} for {str(priority_buy_order.amount)} units from [{priority_sell_order.originator}]")
                    priority_sell_order.amount -= priority_buy_order.amount
                    _ = heapq.heappop(self.__buy_orders)

    def handle_order(self, order):
        # Check the order limit price is outside the valid trading range
        if order.limitprice < 100.0 or order.limitprice > 200.0:
            print(f"Matching Engine with Symbol [{self.symbol}] rejected order from [{order.originator}], Direction: {"Bid" if order.direction == 1 else "Offer"}, Limit Price: {str(order.limitprice)}, and Amount: {str(order.amount)}, Reason: order limit price is outside the valid trading range")
        # Check the order amount is outside the valid range
        elif order.amount > 100 or order.amount < 1:
            print(f"Matching Engine with Symbol [{self.symbol}] rejected order from [{order.originator}], Direction: {"Bid" if order.direction == 1 else "Offer"}, Limit Price: {str(order.limitprice)}, and Amount: {str(order.amount)}, Reason: order amount is outside the valid trading range")
        # If the order is a buy put into buy orders in order
        elif order.direction == 1:
            order.timestamp = time.time()
            heapq.heappush(self.__buy_orders, order)
            print(f"Matching Engine with Symbol [{self.symbol}] accepted order from [{order.originator}], Direction: Bid, Limit Price: {str(order.limitprice)}, and Amount: {str(order.amount)}")
            # Schedule removal of order if ttl is reached
            self.__scheduler.once(dt.timedelta(seconds=5), self.remove_order_ttl, args=(order,))
        # If the order is a sell put into sell orders in order
        else:
            order.timestamp = time.time()
            heapq.heappush(self.__sell_orders, order)
            print(f"Matching Engine with Symbol [{self.symbol}] accepted order from [{order.originator}], Direction: Offer, Limit Price: {str(order.limitprice)}, and Amount: {str(order.amount)}")
            # Schedule removal of order if ttl is reached
            self.__scheduler.once(dt.timedelta(seconds=5), self.remove_order_ttl, args=(order,))
    
    def remove_order_ttl(self, order):
        if order in self.__buy_orders:
            self.__buy_orders.remove(order)
            print(f"Matching Engine with Symbol [{self.symbol}] rejected order from [{order.originator}], Direction: {"Bid" if order.direction == 1 else "Offer"}, Limit Price: {str(order.limitprice)}, and Amount: {str(order.amount)}, Reason: order timeout")
        elif order in self.__sell_orders:
            self.__sell_orders.remove(order)
            print(f"Matching Engine with Symbol [{self.symbol}] rejected order from [{order.originator}], Direction: {"Bid" if order.direction == 1 else "Offer"}, Limit Price: {str(order.limitprice)}, and Amount: {str(order.amount)}, Reason: order timeout")