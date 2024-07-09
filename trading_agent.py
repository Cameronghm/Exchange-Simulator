import numpy as np
from order import Order
from scheduler import Scheduler
import datetime as dt
import uuid

class TradingAgent:
    def __init__(self, average_rate, instrument_list):
        # Average rate for order generation (per second)
        self.__average_rate = average_rate
        self.__instruments = instrument_list
        self.uuid = str(uuid.uuid4().hex)
        self.__scheduler = Scheduler(n_threads=0)

    def run(self):
        # Initial generation of orders
        self.gen_orders()
        # Schedule the new orders to be generated every minute
        self.__scheduler.cyclic(dt.timedelta(minutes=1), self.gen_orders)  
        # Continuously run the Trading Agent to generate new orders
        while True:
            self.__scheduler.exec_jobs()

    def send_order(self, order):
        print(f"[{self.uuid}] Sent an order to Matching Engine with Symbol {order.symbol}, Direction {"Bid" if order.direction == 1 else "Offer"}, Limit Price {order.limitprice}, and Amount {order.amount}")
        self.__instruments[order.symbol].handle_order(order)

    def gen_orders(self):
        # Chooses once at random, unpredictable entropy will be pulled from the OS as seed
        random_generator = np.random.default_rng()
        # Use poisson distribution to get number of orders to be placed in the next minute
        num_of_orders = random_generator.poisson(self.__average_rate)
        for order in range(num_of_orders):
            self.gen_order(random_generator)

    # Called based on average rate
    def gen_order(self, random_generator):
        # Check there are valid matching engines
        if len(self.__instruments) < 1:
            raise Exception("There are no valid matching engines")
        # Gets list of instruments
        instrument = str(random_generator.choice(list(self.__instruments.keys()), size=1, replace=False)[0])
        # Random buy/sell, 0 is buy, 1 is sell
        direction = random_generator.integers(low=0,high=2)
        # Random price, precision of 1 d.p.
        limit_price = round(random_generator.uniform(90.0, 210.0), 1)
        # Random amount
        amount = random_generator.integers(low=1, high=111)
        # Generate Order
        order = Order(self.uuid, instrument, direction, limit_price, amount)
        # Generate time to submit order
        order_time = random_generator.integers(1, 60)
        # Schedule Order Submission, seconds for simplicity
        self.__scheduler.once(dt.timedelta(seconds=int(order_time)), self.send_order, args=(order,))