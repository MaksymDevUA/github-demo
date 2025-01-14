import random, time

from requests_demoblaze import LocustHelpers
from locust import task, between, run_single_user

class SequenceOfTasks(LocustHelpers):
    wait_time = between(4, 6)

    @task
    def choose_and_purchase(self):
        #Enter the website
        self.mainPage()
        time.sleep(random.randint(2, 4))
        #Select random category (Phones, Laptops, Monitors)
        self.chooseCategory()
        time.sleep(random.randint(2, 4))
        #Select random product from selected category for random time times
        for i in range(random.randint(1, 10)):
            self.getItem()
            time.sleep(random.randint(1, 2))
            # Add selected product to the cart
            self.addToCart()
        # Open cart
        self.viewCart()
        # Purchase selected product
        self.deleteAllItems()

if __name__ == "__main__":
    run_single_user(SequenceOfTasks)


