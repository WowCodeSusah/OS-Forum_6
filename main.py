import threading
import random

LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

stack = []
lock = threading.Lock()
producer = False

def producer_function():
    global producer
    for _ in range(MAX_COUNT):
        number = random.randint(LOWER_NUM, UPPER_NUM)
        with lock:
            stack.append(number)
            with open("all.txt", "a") as file:
                file.write(str(number) + "\n")
    producer = True

def consumer_even():
    while not producer:
        with lock:
            if stack and stack[-1] % 2 == 0:
                number = stack.pop()
                with open("even.txt", "a") as file:
                    file.write(str(number) + "\n")
            elif not stack:
                continue
            else:
                continue

def consumer_odd():
    while not producer:
        with lock:
            if stack and stack[-1] % 2 == 1:
                number = stack.pop()
                with open("odd.txt", "a") as file:
                    file.write(str(number) + "\n")
            elif not stack:
                continue
            else:
                continue

if __name__ == "__main__":
    producer_thread = threading.Thread(target=producer_function)
    consumer_even_thread = threading.Thread(target=consumer_even)
    consumer_odd_thread = threading.Thread(target=consumer_odd)

    producer_thread.start()
    consumer_even_thread.start()
    consumer_odd_thread.start()

    producer_thread.join()
    consumer_even_thread.join()
    consumer_odd_thread.join()

    print("All threads finished.")