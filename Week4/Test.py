import asyncio
from time import time, ctime

import httpx


STUDENT_ID = "6710301048"
BASE_URL = "http://172.16.2.117:8088"


async def get_lights(client: httpx.AsyncClient):
    url = f"{BASE_URL}/api/{STUDENT_ID}/lights"

    response = await client.get(url)

    print(f"{ctime()} | GET {url}")
    print(f"HTTP Status: {response.status_code}")
    print(f"ข้อมูลที่ได้รับ: {response.text}")

    if response.status_code == 200:
        return response.json()

    return []


async def turn_on_light(
    client: httpx.AsyncClient,
    light_id: str | int
) -> dict | str:

    url = f"{BASE_URL}/api/{STUDENT_ID}/lights/{light_id}"
    payload = {"status": "ON"}

    try:
        print(f"{ctime()} | กำลังเปิด Light ID: {light_id}")

        response = await client.post(url, json=payload)
        response.raise_for_status()

        result = response.json()

        print(f"{ctime()} | Light {light_id}: เปิดสำเร็จ")
        return result

    except httpx.HTTPStatusError as error:
        print(
            f"{ctime()} | Light {light_id}: "
            f"HTTP {error.response.status_code}"
        )
        print(f"รายละเอียด: {error.response.text}")

        return error.response.text

    except httpx.RequestError as error:
        print(f"{ctime()} | Light {light_id}: เชื่อมต่อไม่ได้")
        return str(error)


async def main() -> None:
    start_time = time()

    async with httpx.AsyncClient(timeout=10.0) as client:
        lights = await get_lights(client)

        print("\nรายการหลอดไฟ:")
        print(lights)

    print(f"\nใช้เวลาตรวจสอบ: {time() - start_time:.2f} วินาที")


if __name__ == "__main__":
    asyncio.run(main())