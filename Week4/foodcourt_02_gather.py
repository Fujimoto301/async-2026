# foodcourt_02_gather.py
import asyncio
from time import time, ctime
from food_utils import send_order_to_kitchen

async def main():
    MY_STUDENT_ID = "6710301048"
    print(f"{ctime()} | --- [Task 2] Practice using gather to wait for all group orders ---")
    start_time = time()

    # 1. Create 3 tasks for ordering from all shops simultaneously.
    task_chicken = asyncio.create_task(send_order_to_kitchen(MY_STUDENT_ID, "hainanese_chicken", "Chicken Rice"))
    task_noodle = asyncio.create_task(send_order_to_kitchen(MY_STUDENT_ID, "noodle", "Wonton Noodles"))
    task_steak = asyncio.create_task(send_order_to_kitchen(MY_STUDENT_ID, "steak", "Sizzling Steak"))

    # 2. Use asyncio.gather() to run all tasks concurrently and collect results.
    results = await asyncio.gather(task_chicken, task_noodle, task_steak)

    # 3. Print each result once all orders are completed.
    for result in results:
        print(f"{ctime()} | [Pickup] Shop: {result['shop']} | Menu: {result['menu']} is ready!")

    print(f"{ctime()} | Total time: {time() - start_time:.2f} seconds (Equals to the slowest dish).")

if __name__ == "__main__":
    asyncio.run(main())