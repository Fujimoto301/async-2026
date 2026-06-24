from time import sleep, ctime, time
import multiprocessing

def update_cup_number(customer_name):
    # ขั้นตอนการประมวลผลหน้าจอ LCD (ใช้เวลา 1 วินาที)
    print(f"{ctime()} | LCD: Processing for customer {customer_name}...")
    sleep(1)
    print(f"{ctime()} | LCD: Done for customer {customer_name}.")

def make_coffee(customer_name):
    # ขั้นตอนการชงกาแฟ (ใช้เวลา 1 วินาที)
    print(f"{ctime()} | Making coffee for {customer_name}...")
    sleep(1)
    print(f"{ctime()} | Coffee ready for {customer_name}!")
    
    # เมื่อชงเสร็จ ให้เรียกฟังก์ชันอัปเดตหน้าจอ LCD ต่อทันทีภายใน Process ของตัวเอง
    update_cup_number(customer_name)

def main():
    queue = ['A', 'B', 'C']
    
    print(f"{ctime()} | === Multi-processing Coffee Machine ===")
    start_time = time()
    
    processes = []
    # ลูปเพื่อสร้างและสั่งรัน Process แยกเด็ดขาดของแต่ละคิวพร้อมกัน
    for customer in queue:
        p = multiprocessing.Process(target=make_coffee, args=(customer,))
        processes.append(p)
        p.start()
        
    # รอให้ทุก Process ประมวลผลเสร็จสิ้นทั้งหมดก่อนสรุปเวลารวม
    for p in processes:
        p.join()
        
    duration = time() - start_time
    print(f"{ctime()} | Total time: {duration:.2f} seconds")

if __name__ == "__main__":
    main()