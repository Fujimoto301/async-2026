# stock_price_httpx.py
# โน้ตกันลืม Assignment 3: ใช้ httpx ดึงราคาหุ้นจริงยิงชน Mock Server แบบ Asynchronous
import asyncio
import httpx  
from time import ctime

async def fetch_stock_price(server_name: str):
    """
    TODO: Assignment 3 - เขียนฟังก์ชันเชื่อมต่อ Mock Server ผ่านระบบเครือข่าย
    1. กำหนดเป้าหมายไปที่พอร์ต 8088 ตามสเปกเซิร์ฟเวอร์ของอาจารย์
    2. ใช้ httpx.AsyncClient() ดึงข้อมูลเพื่อไม่ให้เกิดการ Block สัญญาณ Event Loop
    3. นำข้อมูล JSON (server และ price_usd) มาจัดฟอร์แมตแสดงผล
    """
    url = f"http://172.16.2.117:8088/price/{server_name}"
    
    # ยิงดึงข้อมูลข้ามเน็ตเวิร์กโดยเปิด AsyncClient ป้องกันการเกิด Blocking สัญญาณ Event Loop
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        return f"[{data['server']}] Price: {data['price_usd']} USD"

async def main():
    # สั่งแพ็กคำขอเป็น Task ย่อยรันขนานกันข้ามอินเทอร์เน็ต
    tasks = {
        asyncio.create_task(fetch_stock_price("Alpha"), name="Network-Alpha"),
        asyncio.create_task(fetch_stock_price("Beta"), name="Network-Beta"),
        asyncio.create_task(fetch_stock_price("Gamma"), name="Network-Gamma")
    }
    
    # รันแข่งกัน รอผลตัวเร็วที่สุดตอบกลับคนแรก (Beta)
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    
    # ดึงค่าความเร็วยิงเสร็จคนแรกมาปริ้นโชว์
    for finished_task in done:
        print(f"{ctime()} Winner Result: {finished_task.result()}")
        
    # สั่งยกเลิก Network Requests ของอีกสองตัวที่ช้ากว่าทั้งหมด ป้องกันปัญหารูรั่ว Memory Leak และประหยัด Bandwidth เน็ต
    if pending:
        print(f"{ctime()} Cleaning up {len(pending)} pending tasks...")
        for ongoing_task in pending:
            ongoing_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())