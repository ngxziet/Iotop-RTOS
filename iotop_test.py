#!/usr/bin/env python3
import os
import time
import threading

FILENAME = "iotestfile.dat"
FILESIZE_MB = 100
CHUNK_SIZE = 1024 * 1024  # 1MB

def generate_file():
    """Tạo file test nếu chưa có"""
    if not os.path.exists(FILENAME):
        print("Đang tạo file test...")
        with open(FILENAME, "wb") as f:
            for _ in range(FILESIZE_MB):
                f.write(os.urandom(CHUNK_SIZE))
        print("Đã tạo xong file test.")

def drop_caches():
    """Xóa cache của hệ điều hành để ép đọc đĩa thật"""
    os.system("sync; echo 3 > /proc/sys/vm/drop_caches")

def write_loop():
    """Ghi dữ liệu ngẫu nhiên vào file liên tục"""
    with open(FILENAME, "r+b") as f:
        while True:
            f.seek(0)
            for _ in range(FILESIZE_MB):
                data = os.urandom(CHUNK_SIZE)
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
            time.sleep(0.05)

def read_loop():
    """Đọc dữ liệu từ file, ép hệ điều hành phải đọc từ đĩa"""
    while True:
        drop_caches()
        with open(FILENAME, "rb") as f:
            while chunk := f.read(CHUNK_SIZE):
                pass
        time.sleep(0.05)

def main():
    generate_file()

    # Thread ghi
    threading.Thread(target=write_loop, daemon=True).start()

    # 2 thread đọc
    for _ in range(2):
        threading.Thread(target=read_loop, daemon=True).start()

    print("Đang tạo tải I/O... Nhấn Ctrl+C để thoát.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Kết thúc.")

if __name__ == "__main__":
    main()
