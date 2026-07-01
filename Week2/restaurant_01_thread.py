import threading
from time import sleep, ctime, time


def greet_diners(customer):
    # ทักทายลูกค้าแบบทีละคน (sequential ใน thread หลัก)
    print(f"{ctime()} Greeting for Customer-{customer} ...")
    sleep(1)
    print(f"{ctime()} Greeting for Customer-{customer} ...Done!")


def take_orders(customer):
    print(f"{ctime()}   [Thread-{customer}] Taking Order ...")
    sleep(1)
    print(f"{ctime()}   [Thread-{customer}] Taking Order ...Done!")


def do_cooking(customer):
    print(f"{ctime()}   [Thread-{customer}] Cooking Spaghetti ...")
    sleep(1)
    print(f"{ctime()}   [Thread-{customer}] Cooking Spaghetti ...Done!")


def mini_bar(customer):
    print(f"{ctime()}   [Thread-{customer}] Manage Bar for Drink ...")
    sleep(1)
    print(f"{ctime()}   [Thread-{customer}] Manage Bar for Drink ...Done!")


def serve_customer(customer):
    # งานทั้งหมดของลูกค้าคนหนึ่ง รันเรียงลำดับ "ภายใน" thread ของตัวเอง
    take_orders(customer)
    do_cooking(customer)
    mini_bar(customer)
    print(f"{ctime()}   [Thread-{customer}] All served!")
    print()


if __name__ == "__main__":
    customers = ["A", "B", "C"]
    start_time = time()

    # 1) ทักทายลูกค้าทุกคนก่อน แบบ sequential (thread หลัก)
    for customer in customers:
        greet_diners(customer)

    print()
    print(f"{ctime()} --- All customers greeted. Spawning independent Threads! ---")
    print()

    # 2) สร้าง thread แยกให้แต่ละลูกค้า แล้วรันพร้อมกัน (concurrent)
    threads = [threading.Thread(target=serve_customer, args=(c,)) for c in customers]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    duration = time() - start_time
    print(f"{ctime()} Finished Entire Restaurant Operation in {duration:.2f} seconds.")