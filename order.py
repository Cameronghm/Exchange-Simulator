import uuid

class Order:
    def __init__(self, trading_agent_uuid, symbol, direction, limitprice, amount):
        # # Originating Trading Agent Identity (UUID representing number of Trading Agent)
        self.originator = trading_agent_uuid
        # Symbol/Instrument Identifier (String representing symbol, capping at 4 symbols like NYSE)
        self.symbol = symbol
        # Bid/Offer (1/0 to represent Bid/Offer)
        self.direction = direction
        # Limit Price (1 dp floating point value between 90.0 and 210.0 with 0.1 precision)
        self.limitprice = limitprice
        # Amount (int with value between 1 and 110)
        self.amount = amount
        # Timestamp when order was created
        self.timestamp = None

    # The matching engine will use this to sort the buy and sell orders lists
    def __lt__(self, other_order):
        # If the price is the same then do the comparison on the time to live,
        # the lower the ttl, the older the order
        if self.limitprice == other_order.limitprice:
            return self.timestamp < other_order.timestamp
        # If the order is a buy order then the lower price is prioritised
        if self.direction == 1:
            return self.limitprice > other_order.limitprice
        # If the order is a sell order then the higher price is prioritised
        else:
            return self.limitprice < other_order.limitprice