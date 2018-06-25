# coding: utf-8
import os
import copy
from tqdm import tqdm
import multiprocessing


class MulProcessFileReader:
    def __init__(self, file_name, workers=None, pool_size=1024, batch_size=128):
        self.file_name = file_name
        self.workers = multiprocessing.cpu_count() - 1 if workers is None else workers
        self.pool_size = pool_size
        self._file_size = os.path.getsize(self.file_name)
        self._buffer_size = self._file_size // self.workers + 1
        self.batch_size = batch_size
        self._catch_queue = multiprocessing.Queue(self.pool_size)
        self._start_position = multiprocessing.Value('i', 0)
        self._lock = multiprocessing.Lock()

    def _read_data(self):
        self._lock.acquire()
        cur_start = self._start_position.value
        cur_end = self._start_position.value = self._file_size \
            if (cur_start + self._buffer_size) > self._file_size \
            else cur_start + self._buffer_size
        self._lock.release()
        with open(self.file_name, 'rb') as file_hdl:
            file_hdl.seek(cur_start)
            if cur_start != 0:
                file_hdl.readline()
            samples = []
            idx = 0
            while file_hdl.tell() < cur_end:
                line = file_hdl.readline().decode('utf-8')
                samples.append(self._process_sample(line))
                idx += 1
                if idx % self.batch_size == 0:
                    self._catch_queue.put(copy.deepcopy(samples))
                    samples.clear()
            if len(samples) > 0:
                self._catch_queue.put(copy.deepcopy(samples))
                samples.clear()

    def batch_iterator(self):
        jobs = [multiprocessing.Process(target=self._read_data) for _ in range(self.workers)]
        for job in jobs:
            job.start()

        def check_any_alive():
            return any([x.is_alive() for x in jobs])

        while check_any_alive() or not self._catch_queue.empty():
            if self._catch_queue.empty():
                continue
            yield self._catch_queue.get()

    @staticmethod
    def _process_sample(text):
        # for _ in range(1000):
        #     pass
        return text.strip()


def main():
    file_name = '/mnt/data/weijie/1000w.txt'
    total_cnt = 0
    for item in tqdm(MulProcessFileReader(file_name).batch_iterator()):
        total_cnt += len(item)
    print(total_cnt)


if __name__ == '__main__':
    main()
