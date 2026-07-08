# Assignment 3: Stock Price Race - Live FastAPI + HTTPX
# ประยุกต์ใช้ Concurrency บนระบบเครือข่ายจำลองจริงร่วมกับ httpx
import asyncio
import httpx
from time import ctime

async def fetch_stock_price(server_name: str):
    """
    เชื่อมต่อ Mock Server ผ่านระบบเครือข่าย
    ใช้ httpx.AsyncClient() ดึงข้อมูลเพื่อไม่ให้เกิดการ Block สัญญาณ Event Loop
    """
    # IP หลักของอาจารย์คือ 172.16.2.117 ตามสเปกของรายวิชา
    url = f"http://172.16.2.117:8088/price/{server_name}"

    async with httpx.AsyncClient() as client:
        try:
            # พยายามเชื่อมต่อเซิร์ฟเวอร์หลักของอาจารย์โดยมี timeout 10 วินาที
            response = await client.get(url, timeout=10.0)
            data = response.json()
            return f"[{data['server']}] Price: {data['price_usd']} USD"
        except (httpx.ConnectError, httpx.ConnectTimeout):
            # หากเชื่อมต่อเซิร์ฟเวอร์หลักไม่ได้ ให้ลองเชื่อมต่อผ่าน localhost
            local_url = f"http://localhost:8088/price/{server_name}"
            response = await client.get(local_url, timeout=10.0)
            data = response.json()
            return f"[{data['server']}] Price: {data['price_usd']} USD"

async def main():
    """
    จัดการส่งกลุ่ม Tasks ทำ Concurrency Racing บนเซิร์ฟเวอร์ย่อย Alpha, Beta, Gamma
    และยกเลิกทรัพยากรตัวที่ค้างคา (pending) ทิ้งทันทีเมื่อมีผู้ชนะ
    """
    # 1. สร้าง Tasks สำหรับเริ่มแข่งค้นหาข้อมูลราคารายเซิร์ฟเวอร์ย่อย
    tasks = {
        asyncio.create_task(fetch_stock_price("Alpha"), name="Alpha"),
        asyncio.create_task(fetch_stock_price("Beta"), name="Beta"),
        asyncio.create_task(fetch_stock_price("Gamma"), name="Gamma"),
    }

    # 2. ใช้ asyncio.wait() พร้อมกับ FIRST_COMPLETED เพื่อหาผลลัพธ์จากเซิร์ฟเวอร์แรกที่เสร็จ
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    # 3. แสดงผลลัพธ์ของเซิร์ฟเวอร์ที่ชนะการแข่งขัน
    for finished_task in done:
        result = finished_task.result()
        print(f"{ctime()} Winner Result: {result}")

    # 4. ยกเลิก (cancel) Tasks ที่เหลือที่ยังอยู่ในสถานะ pending
    print(f"{ctime()} Cleaning up {len(pending)} pending tasks...")
    for ongoing_task in pending:
        ongoing_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())