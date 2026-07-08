
import asyncio
import httpx  
from time import ctime

async def fetch_stock_price(server_name: str):
    # หากต้องการส่งงานอาจารย์ ให้สลับไปใช้ IP ปลายทางนี้:
    # url = f"http://172.16.2.117:8088/price/{server_name}"
    url = f"http://127.0.0.1:8088/price/{server_name}"
    
    # เปิดการเชื่อมต่อ HTTP Request แบบ Asynchronous ผ่านไลบรารี httpx เพื่อไม่ให้บล็อกสัญญาณลูปหลัก
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        return f"[{data['server']}] Price: {data['price_usd']} USD"

async def main():
    # สร้างกลุ่ม Task ย่อยเพื่อเตรียมแข่งรันส่งข้อมูลข้ามเน็ตเวิร์กพร้อมกัน
    tasks = {
        asyncio.create_task(fetch_stock_price("Alpha"), name="Network-Alpha"),
        asyncio.create_task(fetch_stock_price("Beta"), name="Network-Beta"),
        asyncio.create_task(fetch_stock_price("Gamma"), name="Network-Gamma")
    }
    
    # ใช้ asyncio.wait ดักรอโดยจะหยุดทันทีเมื่อมีผลตอบกลับชิ้นแรกส่งกลับมาสำเร็จ
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    
    # วนลูปแสดงข้อมูลของฝั่งที่ตอบรับเร็วที่สุด (ซึ่งคาดว่าจะเป็น Beta)
    for finished_task in done:
        print(f"{ctime()} Winner Result: {finished_task.result()}")
        
    # วนลูปเพื่อยกเลิกคำขอบนระบบเน็ตเวิร์กของเซิร์ฟเวอร์ที่เหลือทั้งหมด เพื่อไม่ให้เปลืองพลังงานเครื่องและเครือข่าย
    if pending:
        print(f"{ctime()} Cleaning up {len(pending)} pending tasks...")
        for ongoing_task in pending:
            ongoing_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())