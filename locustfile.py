from locust import HttpUser, task, between
import random as rnd


class UserBehavior(HttpUser):
    wait_time = between(1, 2.5)

    @task(1)
    def say_root(self):
        self.client.get("/")

    @task(2)
    def say_hello(self):
        self.client.get(f"/hello/{self.random_name()}")

    @task(3)
    def cpu_intensive(self):
        n = rnd.randint(30, 36)
        self.client.get(f"/cpu_intensive?n={n}")

    def random_name(self):
        return rnd.choice(['Alice', 'Bob', 'Charlie', 'David'])
