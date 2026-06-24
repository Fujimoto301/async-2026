from time import sleep, ctime, time
import threading

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
    
    # เมื่อชงเสร็จ ให้เรียกฟังก์ชันอัปเดตจอ LCD ต่อทันทีภายใน Thread ของตัวเอง
    update_cup_number(customer_name)

def main():
    queue = ['A', 'B', 'C']
    
    print(f"{ctime()} | === Multi-threading Coffee Machine ===")
    start_time = time()
    
    threads = []
    # ลูปเพื่อสร้างและสั่งรัน Thread แยกของลูกค้าแต่ละคนไปพร้อมๆ กัน
    for customer in queue:
        t = threading.Thread(target=make_coffee, args=(customer,))
        threads.append(t)
        t.start()
        
    # รอให้ Thread ของทุกคนทำงานเสร็จสิ้นทั้งหมดก่อนสรุปเวลา
    for t in threads:
        t.join()
        
    duration = time() - start_time
    print(f"{ctime()} | Total time: {duration:.2f} seconds")

if __name__ == "__main__":
    main()