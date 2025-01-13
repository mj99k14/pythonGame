import socket
import threading
import random
import time

# 서버 설정
SERVER_IP = '210.101.236.189'  # 서버 IP 주소
SERVER_PORT = 12345
clients = []  # 연결된 클라이언트 목록

# 게임 상태 (중앙에서 관리)
game_state = {
    "hoop_y": random.randint(100, 924),  # 골대 Y 좌표
    "hoop_speed": 2,  # 골대 이동 속도
    "players": {  # 플레이어 상태
        "210.101.236.188": {"score": 0, "ball_x": 100, "ball_y": 924},  # 클라이언트 1 초기값
    }
}

# 클라이언트 핸들러
def handle_client(client_socket, client_address):
    global game_state
    client_ip = client_address[0]
    print(f"[연결] 클라이언트 접속: {client_ip}")
    
    # 새로운 클라이언트가 접속하면 초기 상태 등록
    if client_ip not in game_state["players"]:
        game_state["players"][client_ip] = {"score": 0, "ball_x": 100, "ball_y": 924}

    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            # 클라이언트로부터 받은 데이터 처리
            # 데이터 형식: "공_x,공_y,점수"
            ball_x, ball_y, score = data.split(",")
            game_state["players"][client_ip] = {
                "score": int(score),
                "ball_x": float(ball_x),
                "ball_y": float(ball_y),
            }
    except:
        print(f"[오류] 클라이언트 {client_ip} 연결 종료")
    finally:
        # 클라이언트 연결 해제
        print(f"[해제] 클라이언트 연결 해제: {client_ip}")
        clients.remove(client_socket)
        del game_state["players"][client_ip]
        client_socket.close()

# 게임 상태를 클라이언트들에게 전송
def broadcast_game_state():
    global game_state
    while True:
        time.sleep(0.05)  # 20 FPS
        hoop_y = game_state["hoop_y"]
        hoop_speed = game_state["hoop_speed"]

        # 골대 이동
        hoop_y += hoop_speed
        if hoop_y <= 0 or hoop_y >= 924:
            game_state["hoop_speed"] *= -1  # 방향 전환
        game_state["hoop_y"] = hoop_y

        # 현재 게임 상태를 문자열로 변환
        state_str = f"{hoop_y}"
        for ip, player in game_state["players"].items():
            state_str += f";{ip},{player['ball_x']},{player['ball_y']},{player['score']}"

        # 모든 클라이언트에게 전송
        for client_socket in clients:
            try:
                client_socket.sendall(state_str.encode())
            except:
                clients.remove(client_socket)

# 서버 소켓 설정
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(5)
print(f"[시작] 서버 실행 중... IP: {SERVER_IP}, PORT: {SERVER_PORT}")

# 상태 전송 스레드 시작
threading.Thread(target=broadcast_game_state, daemon=True).start()

# 클라이언트 연결 대기
while True:
    client_socket, client_address = server_socket.accept()
    clients.append(client_socket)
    threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()
