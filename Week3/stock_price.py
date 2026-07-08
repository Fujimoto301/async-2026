import asyncio
from time import ctime

# นักเรียนต้องเลือกใช้ asyncio.wait() พร้อมออปชัน return_when=asyncio.FIRST_COMPLETED เท่านั้น (หากใครใช้ gather หรือ wait_for จะไม่ตรงสเปกเงื่อนไขการแข่งส่งข้อมูล)

async def fetch_stock_price(server_name, delay):
    # จำลองระยะเวลาเชื่อมต่อของอินเทอร์เน็ตของสาขาต่างๆ
    await asyncio.sleep(delay)
    # ส่งข้อความผลตอบรับราคาหุ้นเมื่ออ่านสำเร็จ
    return f"[{server_name}] Price: 150 USD"

async def main():
    # แตก Task รันแข่งพร้อมกันทั้ง 3 สาขา และสแตนด์บายใน Event Loop
    tasks = {
        asyncio.create_task(fetch_stock_price("Alpha", 3.0), name="Server-Alpha"),
        asyncio.create_task(fetch_stock_price("Beta", 0.8), name="Server-Beta"),
        asyncio.create_task(fetch_stock_price("Gamma", 1.5), name="Server-Gamma")
    }
    
    # สั่งรอโดยจะดีดตัวออกทันทีที่มี Task แรกเสร็จงานสำเร็จ
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    
    # พิมพ์แจ้งข่าวสารของตัวที่ชนะความเร็ว
    for finished_task in done:
        print(f"{ctime()} Winner Result: {finished_task.result()}")
        
    # พิมพ์เคลียร์คิวยกเลิกงานย่อยตัวที่เหลือที่ทำงานช้ากว่า
    if pending:
        print(f"{ctime()} Cleaning up {len(pending)} pending tasks...")
        for ongoing_task in pending:
            ongoing_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())