🖥️ Python Web Server 🚀

This is a simple multi-threaded Python web server built using sockets. It serves static HTML files from a www/ directory and prevents unauthorized file access.

🌟 Features

🟢 Serves HTML files from the www/ directory.🟢 Handles multiple clients using threads.🟢 Prevents security attacks (blocks ../../ directory traversal attempts).🟢 Returns 404 Not Found for missing files.🟢 Returns 403 Forbidden for unauthorized file access.

🛠 Installation & Usage

📌 1. Clone the Repository

git clone https://github.com/yourusername/python-web-server.git
cd python-web-server

📌 2. Run the Web Server

python server.py

📌 3. Open in a Web Browser

http://localhost:8080/index.html

🚀 Test Cases

✅ 1. Valid File Request (200 OK)

URL to Test: http://localhost:8080/index.htmlExpected Response:

HTTP/1.1 200 OK

❌ 2. Request a Non-Existent File (404 Not Found)

URL to Test: http://localhost:8080/notfound.htmlExpected Response:

HTTP/1.1 404 Not Found

<h1>404 Not Found</h1>

🔒 3. Directory Traversal Attack Attempt (403 Forbidden)

URL to Test: http://localhost:8080/../../etc/passwdExpected Response:

HTTP/1.1 403 Forbidden

<h1>403 Forbidden</h1>

🔒 4. Windows Path Attempt (403 Forbidden)

URL to Test: http://localhost:8080/../../C:/Windows/System32/drivers/etc/hostsExpected Response:

HTTP/1.1 403 Forbidden

<h1>403 Forbidden</h1>

🔒 5. Accessing Hidden Files (403 Forbidden)

URL to Test: http://localhost:8080/.git/configExpected Response:

HTTP/1.1 403 Forbidden

<h1>403 Forbidden</h1>

🔒 6. Attempt to Access Parent Directories (403 Forbidden)

URL to Test: http://localhost:8080/..//..//..//..//etc/passwdExpected Response:

HTTP/1.1 403 Forbidden

<h1>403 Forbidden</h1>

🔒 7. Encoded Path Attack (403 Forbidden)

URL to Test: http://localhost:8080/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwdExpected Response:

HTTP/1.1 403 Forbidden


