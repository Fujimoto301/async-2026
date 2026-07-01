import asyncio
from time import ctime, time


def greet_diners(customer):
    # ทักทายลูกค้าแบบ synchronous (ทีละคน)
    print(f"{ctime()} Greeting for Customer-{customer} ...")
    import time as _t
    _t.sleep(1)
    print(f"{ctime()} Greeting for Customer-{customer} ...Done!")


async def take_order(customer):
    print(f"{ctime()}   [Task-{customer}] Taking Order ...")
    await asyncio.sleep(1)
    print(f"{ctime()}   [Task-{customer}] Taking Order ...Done!")


async def cook_spaghetti(customer):
    print(f"{ctime()}   [Task-{customer}] Cooking Spaghetti ...")
    await asyncio.sleep(1)
    print(f"{ctime()}   [Task-{customer}] Cooking Spaghetti ...Done!")


async def manage_bar(customer):
    print(f"{ctime()}   [Task-{customer}] Manage Bar for Drink ...")
    await asyncio.sleep(1)
    print(f"{ctime()}   [Task-{customer}] Manage Bar for Drink ...Done!")


async def serve_customer(customer):
    # แต่ละ task ของลูกค้า ต้องทำตามลำดับ: order -> cook -> bar
    await take_order(customer)
    await cook_spaghetti(customer)
    await manage_bar(customer)
    print(f"{ctime()}   [Task-{customer}] All served!")
    print()


async def main():
    customers = ["A", "B", "C"]
    start_time = time()

    # 1) ทักทายลูกค้าทุกคนก่อน แบบ sequential (ไม่ async)
    for customer in customers:
        greet_diners(customer)

    print()
    print(f"{ctime()} --- All customers greeted. Scheduling independent Async Tasks! ---")
    print()

    # 2) สร้าง task แยกอิสระให้แต่ละลูกค้า แล้วรันพร้อมกัน (concurrent)
    tasks = [asyncio.create_task(serve_customer(c)) for c in customers]
    await asyncio.gather(*tasks)

    duration = time() - start_time
    print(f"{ctime()} Finished Entire Restaurant Operation in {duration:.2f} seconds.")


if __name__ == "__main__":
    asyncio.run(main())