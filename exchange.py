from matching_engine import MatchingEngine
from trading_agent import TradingAgent
import threading

class Exchange:
    def __init__(self):
        self.matching_engines = {}
        self.trading_agents = []
        self.__trading_agents_threads = []
        self.__matching_engine_threads = []

    def run(self):
        print("Welcome to the Exchange Simulation!")
        try:
            try:
                num_of_matching_engines = int(input("Please enter a number of matching engines to implement: "))
                matching_engines_to_be_created = []
                for matching_engine in range(num_of_matching_engines):
                    symbol = input(f"Please enter the symbol for matching engine {matching_engine+1}: ")
                    matching_engines_to_be_created.append(symbol)
                num_of_trading_agents = int(input("Please enter a number of trading agents to implement: "))
                trading_agents_to_be_created = []
                for trading_agent in range(num_of_trading_agents):
                    average_rate = int(input(f"Please enter the average rate for trading agent {trading_agent+1}: "))
                    trading_agents_to_be_created.append(average_rate)
                for symbol in matching_engines_to_be_created:
                    self.create_matching_engine(symbol)
                for average_rate in trading_agents_to_be_created:
                    self.create_trading_agent(average_rate)
            except Exception as e:
                raise Exception(f"(Error {e}), please enter an integer for the number of agents, average rate of the agents per minute, and number of matching engines")
            print("Starting Simulation!")
        except KeyboardInterrupt:
            print("Exiting loop!")
            for threads in self.__trading_agents_threads:
                threads.join()
            for threads in self.__matching_engine_threads:
                threads.join()
        

    def create_matching_engine(self, symbol):
        try:
            if symbol in self.matching_engines.keys():
                print(f"Already created Matching Engine for: {symbol}")
            else:
                self.matching_engines[symbol] = MatchingEngine(symbol)
                print(f"Created Matching Engine for: {symbol}")
                matching_engine_thread = threading.Thread(target=self.matching_engines[symbol].run)
                matching_engine_thread.start()
                self.__matching_engine_threads.append(matching_engine_thread)
                print(f"Matching Engine with Symbol {symbol} Started")
        except Exception as e:
            raise Exception(f"Can't create matching engine for: {symbol}, raised error: {e}")

    def create_trading_agent(self, average_rate):
        try:
            trading_agent = TradingAgent(average_rate, self.matching_engines)
            self.trading_agents.append(trading_agent)
            print(f"Created Trading Agent with average rate of {average_rate} [{trading_agent.uuid}]")
            trading_agent_thread = threading.Thread(target=self.trading_agents[-1].run)
            trading_agent_thread.start()
            self.__trading_agents_threads.append(trading_agent_thread)
            print(f"Trading Agent [{trading_agent.uuid}] Started")
        except Exception as e:
            raise Exception(f"Can't create trading agent, raised error: {e}")
