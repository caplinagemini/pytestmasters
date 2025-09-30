# example code to be tested
class Car:
    def __init__(self, model, year, top_speed=200, powertrain="petrol"):
        self.model = model
        self.year = year
        self.top_speed = top_speed
        self.powertrain = powertrain

    def get_info(self):
        return f"{self.year} {self.model} with {self.powertrain} powertrain and a top speed of {self.top_speed} km/h"
