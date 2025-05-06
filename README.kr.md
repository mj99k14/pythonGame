
# 🎮 게임 모음 (Game Collection)

이 프로젝트는 **Pygame**을 사용하여 만든 다양한 게임 모음입니다.  
각 게임은 **충돌 판정**, **점프/중력 시스템**, **점수 기록** 등을 포함하며,  
게임을 통해 **Python**과 **Pygame**을 배우며, 게임 개발에 필요한 핵심 기술들을 익힐 수 있습니다.  
**최종 완성된 게임은 농구 게임**입니다.

---

## 🎥 게임 소개 (GIF 포함)

<details>
  <summary>🏀 슛 게임</summary>
  
  <img src="gif/game1.gif" width="600">
  
  **설명:**  
  각도와 파워를 조절해 공을 골대에 넣는 단순한 슈팅 게임입니다.

</details>

<details>
  <summary>⛏ 무한 점프 게임</summary>
  
  <img src="gif/game2.gif" width="600">
  
  **설명:**  
  계속 생성되는 발판을 밟고 최대한 높이 올라가는 점프 게임입니다.

</details>

<details>
  <summary>🍖 아이템 수집 + 장애물 피하기</summary>
  
  <img src="gif/game3.gif" width="600">
  
  **설명:**  
  아이템을 먹고 장애물을 피하며 점점 커지는 캐릭터를 조작하는 게임입니다.

</details>

<details>
  <summary>⏱ 제한 시간 점수 게임</summary>
  
  <img src="gif/game4.gif" width="600">
  
  **설명:**  
  60초 동안 최대한 많은 발판을 밟아 점수를 올리는 게임입니다.

</details>

<details>
  <summary>💥 충돌 후 리셋되는 슈팅 게임</summary>
  
  <img src="gif/game5.gif" width="600">
  
  **설명:**  
  공을 발사해 골대를 맞추는 게임으로, 공이 튕기거나 시간이 지나면 리셋됩니다.

</details>

---

## 🛠 사용 기술

- **Python 3.13.1**
- **pygame** (버전 2.6.1)
- **moviepy** (GIF 제작용)

---

## 💻 개발 환경

이 프로젝트는 **Python 3.13.1**에서 실행됩니다.

**Python 버전 확인 방법:**

1. **터미널/명령 프롬프트 열기**
2. 아래 명령어 입력하여 버전 확인

```bash
python --version
```

또는

```bash
python -V
```

---

## ⌨️ 기본 조작법

| 키         | 기능                  |
|------------|-----------------------|
| ← / →     | 좌우 이동             |
| ↑ / ↓     | 각도 조절 (슛 게임)    |
| 스페이스   | 점프 or 슛 (길게 충전) |
| ESC       | 종료                  |

---

## 📂 폴더 구조

```
project-root/
├── game1/
├── game2/
├── game3/
├── game4/
├── game5/
├── gif/
└── README.kr.md
```

---

## 📝 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE) 하에 배포됩니다.

---
