# Assignment 2: The Stock Price Race - Mock Version (ระบบแข่งดึงข้อมูลราคาหุ้น)
# ใช้ asyncio.wait() พร้อมออปชัน return_when=asyncio.FIRST_COMPLETED
# จำลองการดึงข้อมูลด้วย asyncio.sleep แทน HTTP request จริง
import asyncio
from time import ctime

async def fetch_stock_price(server_name: str, delay: float):
    """
    Coroutine จำลองการดึงข้อมูลราคาหุ้นจากเซิร์ฟเวอร์
    ใช้ asyncio.sleep(delay) เพื่อจำลอง latency ของแต่ละสาขา
    """
    await asyncio.sleep(delay)
    return f"[{server_name}] Price: 150 USD"

async def main():
    """
    สร้าง 3 Tasks พร้อมกันใน Event Loop แล้วใช้ asyncio.wait(FIRST_COMPLETED)
    เพื่อดึงผลลัพธ์ตัวแรกที่เสร็จ แล้วยกเลิกตัวที่เหลือ
    """
    # 1. สร้าง Tasks สำหรับเซิร์ฟเวอร์ Alpha, Beta, Gamma ด้วย delay ที่ต่างกัน
    tasks = {
        asyncio.create_task(fetch_stock_price("Alpha", 3.0), name="Alpha"),
        asyncio.create_task(fetch_stock_price("Beta", 0.8), name="Beta"),
        asyncio.create_task(fetch_stock_price("Gamma", 1.5), name="Gamma"),
    }

    # 2. ใช้ asyncio.wait() พร้อมกับ FIRST_COMPLETED เพื่อหาผลลัพธ์จากเซิร์ฟเวอร์แรกที่เสร็จสิ้น
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    # 3. แสดงผลลัพธ์ของเซิร์ฟเวอร์ที่ชนะการแข่งขัน (ตัวที่เร็วที่สุด)
    for finished_task in done:
        result = finished_task.result()
        print(f"{ctime()} Winner Result: {result}")

    # 4. ยกเลิก (cancel) Tasks ที่เหลือที่ยังอยู่ในสถานะ pending เพื่อป้องกัน Memory Leak
    print(f"{ctime()} Cleaning up {len(pending)} pending tasks...")
    for ongoing_task in pending:
        ongoing_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())
