# MCP Multi-Agent System - 사용 가이드

## 개요

이 프로젝트는 LangGraph와 MCP(Model Context Protocol)를 사용한 멀티 에이전트 시스템입니다.

## 설치

```bash
# 가상환경 활성화
source ../.venv/bin/activate

# 의존성 설치 (이미 설치되어 있다면 생략)
pip install -r ../requirements.txt
```

## 사용 방법

### 1. Jupyter Notebook (대화형)

```bash
jupyter notebook MCP.ipynb
```

Jupyter Notebook에서 셀을 순차적으로 실행하여 에이전트와 대화할 수 있습니다.

### 2. Python CLI (커맨드라인)

```bash
python agent.py
```

터미널에서 대화형 CLI를 통해 에이전트와 대화할 수 있습니다:

```
👤 You: Create a bar chart showing iPhone sales data
🤖 Agent: [에이전트 응답]
```

종료하려면 `quit`, `exit`, 또는 `q`를 입력하세요.

### 3. Streamlit Web Demo (웹 인터페이스)

```bash
streamlit run web_demo.py
```

브라우저가 자동으로 열리며 다음 기능을 사용할 수 있습니다:

- **좌측 사이드바**: 사용 가능한 도구 목록 및 예제 쿼리
- **중앙 영역**: 쿼리 입력 및 에이전트 응답 확인
- **우측 통계**: 도구 개수, 생성된 파일 수 등
- **자동 이미지 표시**: 생성된 차트를 자동으로 표시

## 사용 가능한 도구

### 📚 Document Retrieval
- `retrieve`: iPhone 기술 문서에서 정보 검색

### 🧮 Calculator (5개)
- `calculate`: 수학 표현식 계산
- `percentage_change`: 증감률 계산
- `statistics_summary`: 통계 요약 (평균, 중앙값, 표준편차)
- `currency_convert`: 환율 변환
- `compare_values`: 두 값 비교

### 💻 Code Executor (5개)
- `execute_python`: Python 코드 실행
- `create_visualization`: 데이터 시각화 (차트 생성)
- `analyze_data`: 데이터 분석 (pandas)
- `read_csv`: CSV 파일 읽기
- `save_to_csv`: CSV 파일 저장

### 🔍 Web Search
- `tavily_search_results_json`: 최신 뉴스 및 웹 정보 검색

**총 12개 도구**

## 예제 쿼리

### 예제 1: 간단한 시각화
```
Create a bar chart showing iPhone sales:
- iPhone 17 Pro: 2.8 million
- iPhone 17: 3.5 million
- iPhone 16 Pro: 2.5 million
- iPhone 16: 3.2 million

Title: "iPhone Sales Comparison (Q3 2025)"
Save as: sales_comparison.png
```

### 예제 2: 문서 검색 + 계산
```
1. Retrieve iPhone 17 Pro price in euros from documents
2. Convert to USD using exchange rate 1.08
3. Show the result
```

### 예제 3: 웹 검색 + 분석
```
1. Search for iPhone 17 sales data using web search
2. Extract sales numbers
3. Calculate statistical summary
```

### 예제 4: Python 코드 실행
```
Execute Python code to analyze this data:
sales = [1000, 1200, 1500, 1800, 2000]

Calculate:
1. Mean and standard deviation
2. Growth rate between first and last value
3. Create a line plot showing the trend
```

### 예제 5: 복합 작업
```
Complete analysis task:
1. Retrieve iPhone 17 and iPhone 16 battery capacity from documents
2. Calculate the percentage difference
3. Search for battery life comparison reviews on the web
4. Create a comparison bar chart
5. Save the data to battery_comparison.csv
```

## 출력 파일

모든 생성된 파일은 `output/` 디렉토리에 저장됩니다:

```bash
ls output/
# sales_comparison.png
# battery_comparison.csv
# trend_analysis.png
# ...
```

## 프로그래밍 API

Python 코드에서 직접 사용하기:

```python
from agent import create_mcp_agent, chat_with_agent
import asyncio

# Agent 생성
agent, config, tools = create_mcp_agent()

# 쿼리 실행
async def main():
    await chat_with_agent(
        agent,
        config,
        "Create a bar chart showing iPhone sales data"
    )

# 실행
asyncio.run(main())
```

## 아키텍처

```
┌─────────────────────────────────────────────────┐
│            User Interface                       │
│  (Jupyter / CLI / Streamlit Web)               │
└─────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│         LangGraph ReAct Agent                   │
│         (Claude 3.7 Sonnet)                     │
└─────────────────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┬──────────────┐
        ▼             ▼             ▼              ▼
┌──────────────┐ ┌──────────┐ ┌─────────────┐ ┌─────────┐
│ MCP Server   │ │   MCP    │ │    MCP      │ │ Tavily  │
│     RAG      │ │Calculator│ │Code Executor│ │ Search  │
└──────────────┘ └──────────┘ └─────────────┘ └─────────┘
       │              │              │
       ▼              ▼              ▼
   FAISS DB      Math Ops      Python Runtime
   (PDFs)                      (pandas/numpy/matplotlib)
```

## MCP 서버 상태 확인

각 MCP 서버는 `stdio` transport를 사용하여 통신합니다:

```bash
# RAG 서버 테스트
python mcp_server_rag.py

# Calculator 서버 테스트
python mcp_server_calculator.py

# Code Executor 서버 테스트
python mcp_server_code_executor.py
```

## 트러블슈팅

### 1. 환경 변수 로드 실패
```bash
# .env 파일 확인
cat .env

# 필수 환경 변수
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

### 2. MCP 서버 연결 실패
- Python 경로 확인: `which python`
- 가상환경 활성화 확인: `echo $VIRTUAL_ENV`
- 절대 경로 사용: `/full/path/to/.venv/bin/python`

### 3. matplotlib 오류
```bash
# matplotlib 재설치
pip install --force-reinstall matplotlib
```

### 4. Jupyter Kernel 선택 불가
```bash
# Kernel 등록
python -m ipykernel install --user --name=langgraph-mcp --display-name="Python (langgraph-mcp)"
```

## 추가 리소스

- [LangGraph 문서](https://langchain-ai.github.io/langgraph/)
- [MCP 프로토콜](https://modelcontextprotocol.io/)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [Anthropic Claude](https://www.anthropic.com/claude)

## 라이선스

이 프로젝트는 교육 목적으로 제공됩니다.
