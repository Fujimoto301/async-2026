from time import ctime, time
import asyncio

async def update_cup_number(customer_name):
    # ขั้นตอนการประมวลผลหน้าจอ LCD แบบ Asynchronous (ใช้เวลา 1 วินาที)
    print(f"{ctime()} | LCD: Processing for customer {customer_name}...")
    await asyncio.sleep(1)
    print(f"{ctime()} | LCD: Done for customer {customer_name}.")

async def make_coffee(customer_name):
    # ขั้นตอนการชงกาแฟแบบ Asynchronous (ใช้เวลา 1 วินาที)
    print(f"{ctime()} | Making coffee for {customer_name}...")
    await asyncio.sleep(1)
    print(f"{ctime()} | Coffee ready for {customer_name}!")
    
    # สั่งให้ทำงานขั้นตอนอัปเดตหน้าจอ LCD ต่อแบบ Non-blocking
    await update_cup_number(customer_name)

async def main():
    queue = ['A', 'B', 'C']
    
    print(f"{ctime()} | === Asyncio Coffee Machine ===")
    start_time = time()
    
    tasks = []
    # ลูปเพื่อสร้าง Async Task สำหรับลูกค้าแต่ละคน
    for customer in queue:
        coro = make_coffee(customer)
        task = asyncio.create_task(coro)
        tasks.append(task)
        
    # สั่งรัน Task ทั้งหมดพร้อมกันและรอผลลัพธ์ในรูปแบบขนาน (Concurrent)
    await asyncio.gather(*tasks)
        
    duration = time() - start_time
    print(f"{ctime()} | Total time: {duration:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())