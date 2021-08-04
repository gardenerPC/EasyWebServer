import socket

linkl_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
linkl_client.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
linkl_client.bind(('',2333))
linkl_client.listen(20)

html = ''
data_block1 = 'HTTP/1.1 200 OK\r\n'

def openfile(browser_data):
    loc = browser_data.find('\r\n')
    browser_data =  browser_data[:loc]
    browser_data_list =  browser_data.split(' ')
    browser_data = browser_data_list[1]
    print(browser_data_list)
    if browser_data == '/':
        with open('welcome.html','r') as text:
            while True:
                global html
                html = html + text.read(1024)
                if not(text.read(1024)):
                    break
            return 0
    try:
        with open('.' + browser_data,'r') as text:
            while True:
                # global html
                html = html + text.read(1024)
                if not(text.read(1024)):
                    break
    except FileNotFoundError:
        with open('error.html','r') as text:
            while True:
                # global html
                global data_block1
                data_block1 = 'HTTP/1.1 404 NO\r\n'
                html = html + text.read(1024)
                if not(text.read(1024)):
                    break

# with open('welcome.html','r') as text:
#     while True:
#             # global html
#         html = html + text.read(1024)
#         if not(text.read(1024)):
#             break
while True:
    client,ip_port = linkl_client.accept()
    browser_data = client.recv(1024).decode()
    openfile(browser_data)
    data_block2 = 'Server:PythonWS/3.9\r\n\r\n' + html + '\r\n'
    data = data_block1 + data_block2
    if not browser_data:
        client.close()
        continue
    print(browser_data)
    html = ''
    data_block1 = 'HTTP/1.1 200 OK\r\n'
    client.send(data.encode())
    client.close()

linkl_client.close()