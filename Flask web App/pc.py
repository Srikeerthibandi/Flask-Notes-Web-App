import threading
import time
import random
from queue import Queue

# The shared buffer with a maximum size
BUFFER_SIZE = 10
SHARED_QUEUE = Queue(BUFFER_SIZE)

# Sentinel value to signal consumers that production is complete
SENTINEL = None

class ProducerThread(threading.Thread):
    def run(self):
        print('Producer: Running')
        for i in range(10):
            item = f'item_{i}'
            # put() blocks if the queue is full until a free slot is available
            SHARED_QUEUE.put(item) 
            print(f'>producer added {item}')
            time.sleep(random.random()) # Simulate work

        # Signal that no further items will be produced
        SHARED_QUEUE.put(SENTINEL)
        print('Producer: Done')

class ConsumerThread(threading.Thread):
    def run(self):
        print('Consumer: Running')
        while True:
            # get() blocks if the queue is empty until an item is available
            item = SHARED_QUEUE.get()
            if item is SENTINEL:
                break # Exit loop when sentinel value is received

            print(f'>consumer got {item}')
            time.sleep(random.random()) # Simulate work
            # In a real-world scenario, you might use queue.task_done() here
            # and queue.join() in the main thread

        print('Consumer: Done')

# Main execution
if __name__ == '__main__':
    producer = ProducerThread()
    consumer = ConsumerThread()

    producer.start()
    consumer.start()

    # Wait for both threads to finish
    producer.join()
    consumer.join()

    print('Main thread: All tasks finished')
