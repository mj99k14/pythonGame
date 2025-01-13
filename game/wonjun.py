import socket
import threading

def handle_client(client_socket, opponent_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if data:
                opponent_socket.sendall(data)
            else:
                break
        except:
            break
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('210.101.236.186', 12345))
    server_socket.listen(2)
    print("서버가 대기 중입니다...")

    clients = []
    for _ in range(2):
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        print(f"{addr}와 연결되었습니다.")

    thread1 = threading.Thread(target=handle_client, args=(clients[0], clients[1]))
    thread2 = threading.Thread(target=handle_client, args=(clients[1], clients[0]))
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    server_socket.close()

if __name__ == "__main__":
    main()
