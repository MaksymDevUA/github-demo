from locust import HttpUser, task, between
import uuid, json, random

class LocustHelpers(HttpUser):
    abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cat_rand_list = ["notebook", "phone", "monitor"]
        self.num_of_items_in_cat = 0
        self.ids_in_cat = []
        self.rand_item = 0
        self.ids_in_cart = [] #ids in cart
        self.generated_id = str(uuid.uuid4())

    def mainPage(self):
        print("mainPage")
        self.client.get("https://www.demoblaze.com/index.html")
        self.client.get("https://api.demoblaze.com/entries")

    def chooseCategory(self):
        print("chooseCategory")
        self.rand_cat = self.cat_rand_list[random.randint(0, 2)]
        options_response = self.client.options("https://api.demoblaze.com/bycat") # Do we need OPTIONS in requests? or post enough?
        assert options_response.status_code == 200, "OPTIONS request failed"

        post_response = self.client.post("https://api.demoblaze.com/bycat",
                                    json={"cat":self.rand_cat})
        assert post_response.status_code == 200, f"Expected 200 but got {post_response.status_code}"
        # items_resp_to_dict = json.loads(post_response.text)
        items_resp_to_dict = post_response.json()
        self.ids_in_cat = [item['id'] for item in items_resp_to_dict['Items']]
        self.num_of_items_in_cat = (len(self.ids_in_cat))

    def getItem(self):
        print("getItem")
        self.rand_item = random.choice(self.ids_in_cat)
        # print(self.ids_in_cat)
        # print(self.rand_item)
        response_get = self.client.get(f"https://www.demoblaze.com/prod.html?idp_={self.rand_item}")
        assert response_get.status_code == 200, "GET request failed"
        options_response = self.client.options("https://api.demoblaze.com/view")
        assert options_response.status_code == 200, "OPTIONS request failed"
        post_response = self.client.post("https://api.demoblaze.com/view",
                         json={"id":self.rand_item})
        assert post_response.status_code == 200, "POST request failed"

        print(f"response getItem{post_response.status_code}")
        print(f"response text{post_response.text}")

    def addToCart(self):
        print("addToCart")
        options_response = self.client.options("https://api.demoblaze.com/addtocart")
        assert options_response.status_code == 200, "OPTIONS request failed"
        post_response = self.client.post("https://api.demoblaze.com/addtocart",
                         json={"cookie":"user=96b0f348-fdc9-1bb6-2b8b-15e529cd43c8", "id": self.generated_id,
                               "prod_id": self.rand_item, "flag": False})
        assert post_response.status_code == 200, "POST request failed"
        print(post_response.text)

    def viewCard(self):
        print("viewCard")
        options_response = self.client.options_response("https://api.demoblaze.com/viewcart")
        assert options_response.status_code == 200, "OPTIONS request failed"
        post_response = self.client.post(" https://api.demoblaze.com/viewcart", json={"cookie":"user=96b0f348-fdc9-1bb6-2b8b-15e529cd43c8",
                                                                                 "flag": False})
        assert post_response.status_code == 200, "POST request failed"

        print(post_response.text)

    def viewCart(self):
        print("viewCart")
        get_response = self.client.get("https://www.demoblaze.com/cart.html")
        assert get_response.status_code == 200, "GET request failed"
        options_response = self.client.options("https://api.demoblaze.com/viewcart")
        assert options_response.status_code == 200, "OPTIONS request failed"
        post_response = self.client.post("https://api.demoblaze.com/viewcart", json={"cookie": "user=96b0f348-fdc9-1bb6-2b8b-15e529cd43c8", "flag":False})
        assert post_response.status_code == 200, "POST request failed"
        items_in_cart = json.loads(post_response.text)
        self.id_in_cart = [item['id'] for item in items_in_cart['Items']]
        print(self.ids_in_cart)

    def deleteAllItems(self): #aka purchasingItems
        print("deleteAllItems")
        options_response = self.client.options("https://api.demoblaze.com/deleteitem")
        assert options_response.status_code == 200, "OPTIONS request failed"
        for item in self.id_in_cart:
            print(f"delete:{item}")
            post_response = self.client.post("https://api.demoblaze.com/deleteitem",
                                    json={"id":item})
            assert post_response.status_code == 200, "POST request failed"
            print(f"{item} = {post_response.text}")
