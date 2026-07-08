# Assignment 1: The Smart Courier System (ระบบส่งพัสดุด่วน)
# Delivery System: นักศึกษาต้องเขียน try...except CancelledError ได้ถูกต้อง 
# และใช้ .get_name(), .cancel(), และ .cancelled() ได้
import asyncio
from time import ctime

async def delivery_task(package_id: str, duration: float):
    """
    Coroutine จำลองการส่งของด้วย asyncio.sleep(duration)
    พิมพ์ข้อความเมื่อเริ่มส่ง และเมื่อส่งเสร็จสิ้น return ข้อความ Delivered
    """
    print(f"{ctime()} Courier started delivering {package_id}...")
    try:
        await asyncio.sleep(duration)
        print(f"{ctime()} Package {package_id} Delivered!")
        return f"Package {package_id} Delivered!"
    except asyncio.CancelledError:
        # ดักจับ CancelledError เมื่อ task ถูกยกเลิก
        print(f"{ctime()} Delivery Canceled! Returning package to warehouse.")
        raise  # ต้อง raise ต่อเพื่อให้ task เข้าสู่สถานะ cancelled จริง

async def main():
    # 1. สร้าง Task จาก delivery_task โดยส่งค่า package_id="P001" และ duration=5.0
    #    และตั้งชื่อ Task นี้ว่า "Express-Courier"
    task = asyncio.create_task(
        delivery_task(package_id="P001", duration=5.0),
        name="Express-Courier"
    )
    
    # 2. จำลองว่าระหว่างที่พัสดุกำลังเดินทาง (ผ่านไป 2 วินาที)
    #    ให้ทำการตรวจสอบด้วยคำสั่งฝั่งแฝง ว่า Task นี้เสร็จหรือยัง (.done())
    #    และสั่งพิมพ์ชื่อของ Task ปัจจุบันออกมาดูบนหน้าจอ
    await asyncio.sleep(2)
    print(f"{ctime()} Checking task '{task.get_name()}'. Is it done? {task.done()}")
    
    # 3. หากพบว่าส่งของนานเกินไป (ผ่านไป 2 วินาทีแล้วยังไม่เสร็จ)
    #    ให้โปรแกรมหลักทำการยกเลิกงานนั้นทันทีด้วย .cancel()
    if not task.done():
        print(f"{ctime()} Taking too long! Canceling the task...")
        task.cancel()
    
    # 4. รอให้ task จบการทำงาน (ไม่ว่าจะสำเร็จหรือถูก cancel)
    try:
        await task
    except asyncio.CancelledError:
        pass
    
    # 5. ตรวจสอบสถานะตัวแปรภายนอกว่า .cancelled() เป็น True หรือไม่
    print(f"{ctime()} Final verify: Is task officially canceled? {task.cancelled()}")

if __name__ == "__main__":
    asyncio.run(main())
