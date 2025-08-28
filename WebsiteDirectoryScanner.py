# Website Directory Scanner

# Usage example:
# python WebsiteDirectoryScanner.py --url http://testphp.vulnweb.com/ --wordlist wordlist.txt --threads 10 --extensions .php,.bak,.txt

import argparse
import requests
import threading
from queue import Queue
from tqdm import tqdm
import os

RESULT_FILE = "result.txt"

class Scanner:
    # Tool menerima input: --url, --wordlist, --threads, --extensions
    def __init__(self, url, wordlist, threads, extensions):
        self.url = url.rstrip('/')
        self.wordlist = wordlist
        self.threads = threads
        self.extensions = extensions
        self.queue = Queue()
        self.found = []
        self.lock = threading.Lock()

    # --wordlist (file berisi daftar path, contoh: admin, login, uploads)
    def load_wordlist(self):
        with open(self.wordlist, 'r') as f:
            words = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
        return words

    # Tool melakukan HTTP request ke setiap path (url + "/" + wordlist_entry)
    # --extensions untuk mencoba otomatis ekstensi (misal .php, .bak, .txt)
    def enqueue_paths(self, words):
        for word in words:
            self.queue.put((word, None))
            for ext in self.extensions:
                self.queue.put((word, ext))

    # --threads untuk concurrency sederhana (menggunakan threading)
    # Jika response status 200 / 301 / 302, maka hasilnya disimpan ke file result.txt
    def scan_worker(self, pbar):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        while not self.queue.empty():
            try:
                word, ext = self.queue.get_nowait()
            except:
                break
            path = word + (ext if ext else '')
            target_url = f"{self.url}/{path}"
            try:
                resp = requests.get(target_url, allow_redirects=False, timeout=10, headers=headers)
                # Jika response status 200 / 301 / 302
                if resp.status_code in [200, 301, 302]:
                    with self.lock:
                        self.found.append((target_url, resp.status_code))
                        print(f"[+] Found: {target_url} ({resp.status_code})")
            except Exception:
                pass
            finally:
                # Tambahkan progress bar
                pbar.update(1)
                self.queue.task_done()

    # --threads untuk concurrency sederhana
    # Tambahkan progress bar
    def run(self):
        words = self.load_wordlist()
        self.enqueue_paths(words)
        total = self.queue.qsize()
        pbar = tqdm(total=total, desc="Scanning", ncols=80)
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=self.scan_worker, args=(pbar,))
            t.daemon = True
            t.start()
            threads.append(t)
        self.queue.join()
        for t in threads:
            t.join()
        pbar.close()
        self.save_results()

    # Hasilnya disimpan ke file result.txt
    def save_results(self):
        with open(RESULT_FILE, 'w') as f:
            for url, code in self.found:
                f.write(f"{url} ({code})\n")
        print(f"\nResults saved to {RESULT_FILE}")


# Tool menerima input: --url, --wordlist, --threads, --extensions
def parse_args():
    parser = argparse.ArgumentParser(description="Website Directory Scanner")
    # --url (target website, contoh: http://testphp.vulnweb.com/)
    parser.add_argument('--url', required=True, help='Target website URL')
    # --wordlist (file berisi daftar path, contoh: admin, login, uploads)
    parser.add_argument('--wordlist', required=True, help='Wordlist file')
    # --threads untuk concurrency sederhana
    parser.add_argument('--threads', type=int, default=10, help='Number of threads')
    # --extensions untuk mencoba otomatis ekstensi (misal .php, .bak, .txt)
    parser.add_argument('--extensions', type=str, default='', help='Comma-separated extensions (e.g. .php,.bak,.txt)')
    return parser.parse_args()


def main():
    args = parse_args()
    # --extensions untuk mencoba otomatis ekstensi
    extensions = [e.strip() for e in args.extensions.split(',') if e.strip()]
    # Tool menerima input: --url, --wordlist, --threads, --extensions
    scanner = Scanner(args.url, args.wordlist, args.threads, extensions)
    scanner.run()

if __name__ == "__main__":
    main()
