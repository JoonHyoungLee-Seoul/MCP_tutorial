# 🚀 Quick Start Guide

## 3가지 사용 방법

### 1️⃣ Jupyter Notebook (권장 - 대화형)

```bash
# Jupyter Notebook 실행
jupyter notebook MCP.ipynb
```

**장점:**
- 셀 단위 실행으로 단계별 확인 가능
- 출력 결과를 바로 볼 수 있음
- 이미지 자동 표시

---

### 2️⃣ Python CLI (터미널)

```bash
# CLI 모드로 실행
python agent.py
```

**사용 예시:**
```
👤 You: Create a bar chart showing iPhone sales data
🤖 Agent: [응답]

👤 You: quit
👋 Goodbye!
```

**장점:**
- 빠른 테스트에 적합
- 스크립트 통합 가능

---

### 3️⃣ Streamlit Web Demo (웹 브라우저)

```bash
# Streamlit 웹 앱 실행
streamlit run web_demo.py
```

브라우저에서 `http://localhost:8501` 자동 오픈

**장점:**
- 직관적인 GUI
- 예제 쿼리 버튼 제공
- 생성된 이미지 자동 표시
- 실시간 도구 사용 현황 확인

---

## 빠른 테스트

### 테스트 1: 시각화
```
Create a bar chart showing:
- iPhone 17: 3.5M units
- iPhone 16: 3.2M units
Save as test_chart.png
```

### 테스트 2: 문서 검색
```
What is the battery capacity of iPhone 17 Pro?
```

### 테스트 3: 계산
```
Calculate the percentage increase from 1000 to 1400
```

### 테스트 4: Python 실행
```
Execute Python: print("Hello from MCP Agent!")
import pandas as pd
df = pd.DataFrame({'x': [1,2,3], 'y': [4,5,6]})
print(df)
```

### 테스트 5: 복합 작업
```
1. Retrieve iPhone 17 Pro price from documents
2. Convert USD to EUR using rate 0.92
3. Show the result
```

---

## 출력 확인

```bash
# 생성된 파일 확인
ls -lh output/

# 이미지 뷰어로 열기 (macOS)
open output/test_chart.png

# CSV 파일 확인
cat output/battery_comparison.csv
```

---

## 시스템 구성

```
📦 lee_mcp_tutorial/
├── 📓 MCP.ipynb                    # Jupyter Notebook
├── 🐍 agent.py                     # Python CLI
├── 🌐 web_demo.py                  # Streamlit Web Demo
├── 🔧 utils.py                     # 유틸리티 함수
├── 🤖 mcp_server_rag.py            # RAG 서버
├── 🧮 mcp_server_calculator.py     # 계산기 서버
├── 💻 mcp_server_code_executor.py  # 코드 실행 서버
├── 📁 data/                        # PDF 문서
├── 📁 output/                      # 생성된 파일
└── 📄 .env                         # 환경 변수
```

---

## 환경 변수 설정

`.env` 파일 필수 내용:

```bash
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
```

---

## 문제 해결

### ❌ "No module named 'streamlit'"
```bash
pip install streamlit
```

### ❌ "ANTHROPIC_API_KEY not found"
```bash
# .env 파일 확인
cat .env

# 환경 변수 직접 설정
export ANTHROPIC_API_KEY=sk-ant-...
```

### ❌ MCP 서버 연결 실패
```bash
# Python 경로 확인
which python

# agent.py에서 venv_path 수정
venv_path = "/full/path/to/.venv/bin/python"
```

---

## 다음 단계

1. ✅ **Quick Start** 완료
2. 📖 [USAGE_GUIDE.md](./USAGE_GUIDE.md) - 상세 사용법
3. 🧮 [CALCULATOR_USAGE.md](./CALCULATOR_USAGE.md) - 계산기 도구
4. 💻 [CODE_EXECUTOR_USAGE.md](./CODE_EXECUTOR_USAGE.md) - 코드 실행 도구
5. 📝 [NOTEBOOK_EXAMPLES.md](./NOTEBOOK_EXAMPLES.md) - 예제 모음

---

## 🎯 추천 워크플로우

**초보자:**
1. Jupyter Notebook으로 시작 (`MCP.ipynb`)
2. 예제 셀을 하나씩 실행
3. 출력 결과 확인

**개발자:**
1. Python CLI로 빠른 테스트 (`agent.py`)
2. 스크립트에 통합

**데모/프레젠테이션:**
1. Streamlit Web Demo 실행 (`web_demo.py`)
2. 브라우저에서 시연

---

**Happy Coding! 🚀**
