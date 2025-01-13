import socket

# 클라이언트 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버 연결
try:
    client_socket.connect(('210.101.236.189', 12345))  # 서버 IP와 포트 번호
    print("서버에 성공적으로 연결되었습니다.")

    # 데이터 송수신
    while True:
        message = input("서버로 보낼 메시지: ")
        if message == 'quit':  # 'quit' 입력 시 연결 종료
            break
        client_socket.sendall(message.encode())  # 서버로 데이터 전송
        data = client_socket.recv(1024).decode()  # 서버로부터 데이터 수신
        print(f"서버로부터 받은 응답: {data}")
except ConnectionRefusedError:
    print("서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
except Exception as e:
    print(f"클라이언트 에러: {e}")
finally:
    client_socket.close()
