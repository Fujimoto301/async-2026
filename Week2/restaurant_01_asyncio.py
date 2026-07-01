import asyncio
from time import time, ctime

async def greet_diners(customer):
    print(f"{ctime()} Greeting for Customer-{customer} ...")
    await asyncio.sleep(1)
    print(f"{ctime()} Greeting for Customer-{customer} ...Done!")


async def customer_private_workflow(customer):
    # Take Order
    print(f"{ctime()}  [Task-{customer}] Taking Order ...")
    await asyncio.sleep(1)
    print(f"{ctime()}  [Task-{customer}] Taking Order ...Done!")

    # Do Cooking
    print(f"{ctime()}  [Task-{customer}] Cooking Spaghetti ...")
    await asyncio.sleep(1)
    print(f"{ctime()}  [Task-{customer}] Cooking Spaghetti ...Done!")

    # Manage Bar
    print(f"{ctime()}  [Task-{customer}] Manage Bar for Drink ...")
    await asyncio.sleep(1)
    print(f"{ctime()}  [Task-{customer}] Manage Bar for Drink ...Done!")
    print(f"{ctime()}  [Task-{customer}] All served!\n")

async def main():
    start_time = time()
    customers = ['A', 'B', 'C']

    for customer in customers:
        await greet_diners(customer)

    print(f"\n{ctime()} --- All customers greeted. Scheduling independent Async Tasks! ---\n")

    tasks = []
    for customer in customers:
        task = asyncio.create_task(customer_private_workflow(customer))
        tasks.append(task)

    await asyncio.gather(*tasks)

    duration = time() - start_time
    print(f"{ctime()} Finished Cooking in {duration:0.2f} seconds.")

if __name__ == "__main__":
    asyncio.run(main())