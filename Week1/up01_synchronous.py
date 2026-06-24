from time import sleep, ctime, time

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
    
    # สั่งทำงานขั้นตอนแสดงผลหน้าจอ LCD ต่อทันที
    update_cup_number(customer_name)

def main():
    queue = ['A', 'B', 'C']
    
    print(f"{ctime()} | === Synchronous Coffee Machine ===")
    start_time = time()
    
    # ทำงานเรียงลำดับตามคิวเดี่ยวทีละคน (Synchronous)
    for customer in queue:
        make_coffee(customer)
        
    duration = time() - start_time
    print(f"{ctime()} | Total time: {duration:.2f} seconds")

if __name__ == "__main__":
    main()