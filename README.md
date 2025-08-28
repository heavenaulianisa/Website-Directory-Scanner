# Website Directory Scanner

A Python tool for scanning website directories using wordlists. This tool helps discover hidden directories and files on web servers for security testing purposes.

## Features

- Multi-threaded scanning for faster results
- Support for custom wordlists
- File extension scanning (.php, .html, .txt, etc.)
- Progress bar with real-time updates
- Automatic result saving
- Customizable thread count
- HTTP status code filtering

## 📖 Usage

### Basic Command Structure
```
python WebsiteDirectoryScanner.py --url <target_url> --wordlist <wordlist_file> [options]
```

### Parameters
- `--url`: Target website URL (required)
- `--wordlist`: Path to wordlist file (required)
- `--threads`: Number of threads (default: 10)
- `--extensions`: File extensions to test (e.g., .php,.html,.txt)
- `--help`: Show help message

### Example Commands
```
# Basic scan
python WebsiteDirectoryScanner.py --url http://example.com --wordlist wordlist.txt

# Scan with custom threads
python WebsiteDirectoryScanner.py --url http://example.com --wordlist wordlist.txt --threads 20

# Scan with file extensions
python WebsiteDirectoryScanner.py --url http://example.com --wordlist wordlist.txt --extensions .php,.html,.txt

# Full scan example
python WebsiteDirectoryScanner.py --url http://testphp.vulnweb.com --wordlist wordlist.txt --threads 15 --extensions .php,.asp,.txt,.bak
```

### Legal Testing Targets

**Safe Sites for Testing:**
1. **http://testphp.vulnweb.com** - Acunetix test site
2. **http://httpbin.org** - HTTP testing service  
3. **http://demo.testfire.net** - IBM Altoro Mutual demo
4. **https://juice-shop.herokuapp.com** - OWASP Juice Shop (intentionally vulnerable web app)
5. **Your own websites** - Always the safest option!

### Expected Results

#### Successful Output Example:
```
Scanning: 100%|████████████| 150/150 [00:30<00:00, 5.0it/s]
[+] Found: http://testphp.vulnweb.com/admin (200)
[+] Found: http://testphp.vulnweb.com/images (301)
[+] Found: http://testphp.vulnweb.com/login.php (200)

Results saved to result.txt
```

#### Output Files
- **result.txt**: Contains all discovered directories/files
- **Console output**: Real-time progress and findings

## Sample Wordlists

### Download Popular Wordlists
```
# SecLists (recommended)
wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt

# DirBuster wordlist
wget https://raw.githubusercontent.com/daviddias/node-dirbuster/master/lists/directory-list-2.3-medium.txt
```

## Understanding Results

### HTTP Status Codes:
- **200**: Found (accessible)
- **301/302**: Redirect (might be interesting)
- **403**: Forbidden (exists but restricted)
- **404**: Not found
- **500**: Server error

### Result Analysis:
```
# View results
Get-Content result.txt

# Count findings
(Get-Content result.txt).Count

# Filter by status code
Select-String "200" result.txt
Select-String "403" result.txt
```
