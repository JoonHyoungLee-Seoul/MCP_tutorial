# LangGraph MCP RAG Agent Tutorial

LangGraph와 MCP (Model Context Protocol)를 활용한 RAG (Retrieval-Augmented Generation) 에이전트 튜토리얼입니다.

## 프로젝트 개요

이 프로젝트는 다음 기술들을 통합하여 강력한 AI 에이전트를 구축하는 방법을 보여줍니다:
- **LangGraph**: 복잡한 에이전트 워크플로우 구축
- **MCP (Model Context Protocol)**: 도구 및 외부 시스템 통합
- **RAG (Retrieval-Augmented Generation)**: 문서 기반 정보 검색
- **TavilySearch**: 실시간 웹 검색
- **Claude 3.5 Sonnet**: Anthropic의 최신 LLM 모델

## 주요 기능

### 1. 다중 도구 통합 (총 12개 도구!)
- **RAG Retriever** (1개): PDF 문서에서 정보 검색
- **Calculator** (5개): 수학 계산, 통계, 환율 변환, 값 비교
- **Code Executor** (5개): Python 코드 실행, 데이터 분석, 시각화
- **TavilySearch** (1개): 최신 뉴스 및 웹 정보 검색
- **자동 도구 선택**: 에이전트가 쿼리에 따라 적절한 도구 자동 선택

### 2. MCP 서버 구현
#### 📚 RAG Retriever MCP (`mcp_server_rag.py`)
- FAISS 벡터 스토어 기반 문서 검색
- OpenAI Embeddings를 통한 텍스트 임베딩
- 전역 캐싱으로 성능 최적화
- PDF 문서 일괄 로딩

#### 🧮 Calculator MCP (`mcp_server_calculator.py`)
- 수학 표현식 계산 (삼각함수, 로그, 제곱근 등)
- 퍼센트 증감률 계산
- 통계 요약 (평균, 중앙값, 표준편차)
- 환율 변환
- 값 비교 분석

#### 💻 Code Executor MCP (`mcp_server_code_executor.py`)
- Python 코드 안전 실행 (pandas, numpy, matplotlib)
- 데이터 시각화 (5가지 차트: line, bar, scatter, pie, hist)
- 데이터 분석 (통계, 그룹화, 정렬, 상관관계)
- CSV 파일 읽기/쓰기

### 3. 실시간 스트리밍
- 에이전트 실행 과정 실시간 모니터링
- 도구 사용 추적 (선택 및 실행)
- 색상 코딩된 출력으로 가독성 향상

## 설치 방법

### 1. 필수 요구사항
- Python 3.12+
- Virtual Environment (venv)
- Jupyter Notebook

### 2. 의존성 설치

```bash
# 가상환경 활성화
source ../.venv/bin/activate

# 필수 패키지 설치 (부모 디렉토리에서)
cd ..
pip install -r requirements.txt
```

### 3. Jupyter Kernel 등록

```bash
# 가상환경을 Jupyter 커널로 등록
python -m ipykernel install --user --name=langgraph-mcp --display-name="Python (langgraph-mcp)"
```

### 4. 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 추가하세요:

```bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_PROJECT=LangGraph-MCP-Agents
TAVILY_API_KEY=your_tavily_api_key_here
```

**중요**: `OPENAI_BASE_URL`이 시스템 환경변수에 설정되어 있으면 제거하세요. 이 프로젝트는 OpenAI API를 직접 사용합니다.

## 사용 방법

### 1. PDF 문서 준비

`data/` 디렉토리에 검색할 PDF 문서를 저장하세요:

```bash
data/
├── document1.pdf
├── document2.pdf
└── ...
```

### 2. Jupyter Notebook 실행

```bash
jupyter notebook MCP.ipynb
```

### 3. 셀 실행 순서

#### Cell 0: 환경 설정
```python
# 작업 디렉토리 및 환경 변수 로드
```

#### Cell 3: 도구 초기화
```python
# MCP 클라이언트 및 TavilySearch 설정
# MultiServerMCPClient를 사용하여 session 자동 관리
```

#### Cell 5: 에이전트 생성
```python
# ReAct 에이전트 생성 및 설정
```

#### Cell 7: TavilySearch 테스트
```python
# 최신 뉴스 검색 예제
await astream_graph(
    agent,
    {"messages": "Tell me about iPhone 17 sales..."},
    config=config
)
```

#### Cell 9: RAG Retriever 테스트
```python
# 문서에서 정보 검색 예제
await astream_graph(
    agent,
    {"messages": "What are the specifications of iPhone 17 Pro Camera?"},
    config=config
)
```

#### Cell 11: 통합 사용
```python
# 두 도구를 모두 활용하는 예제
await astream_graph(
    agent,
    {"messages": "First retrieve color options, then search for news..."},
    config=config
)
```

## 파일 구조

```
lee_mcp_tutorial/
├── MCP.ipynb                      # 메인 Jupyter Notebook
├── mcp_server_rag.py              # 📚 RAG Retriever MCP 서버
├── mcp_server_calculator.py       # 🧮 Calculator MCP 서버
├── mcp_server_code_executor.py    # 💻 Code Executor MCP 서버
├── utils.py                       # 유틸리티 함수 (스트리밍, 도구 추적)
├── .env                           # 환경 변수 설정
├── data/                          # PDF 문서 저장 디렉토리
│   ├── document1.pdf
│   └── ...
├── output/                        # 생성된 차트 및 파일
│   ├── *.png                     # 시각화 차트
│   └── *.csv                     # 데이터 파일
├── README_KOR.md                  # 한국어 README
├── README.md                      # 영어 README
├── CALCULATOR_USAGE.md            # Calculator MCP 사용 가이드
├── CODE_EXECUTOR_USAGE.md         # Code Executor MCP 사용 가이드
└── NOTEBOOK_EXAMPLES.md           # 노트북 예제 모음
```

### 주요 파일 설명

#### `mcp_server_rag.py`
- FastMCP 기반 MCP 서버
- PDF 문서 로딩 (DirectoryLoader)
- FAISS 벡터 스토어 생성
- OpenAI Embeddings 사용
- 전역 캐싱으로 retriever 재사용
- `retrieve(query: str)` 도구 제공

**핵심 기능**:
```python
@mcp.tool()
async def retrieve(query: str) -> str:
    """문서 데이터베이스에서 정보 검색"""
    global _retriever
    if _retriever is None:
        _retriever = create_retriever()
    retrieved_docs = _retriever.invoke(query)
    return "\n".join([doc.page_content for doc in retrieved_docs])
```

#### `utils.py`
- `astream_graph()`: LangGraph 실행 스트리밍 함수
- `print_tool_info()`: 도구 사용 추적 및 출력
- 색상 코딩된 출력 (🔧 도구 선택, ✅ 도구 실행)

#### `MCP.ipynb`
- Cell 0: 환경 설정 및 dotenv 로드
- Cell 1: 단일 MCP 도구 사용 예제
- Cell 3: MCP + TavilySearch 통합 (MultiServerMCPClient 사용)
- Cell 5: ReAct 에이전트 생성
- Cell 7-11: 다양한 사용 예제

## 기술 스택

### LLM & AI Framework
- **Claude 3.5 Sonnet** (`claude-3-7-sonnet-latest`): Anthropic의 최신 대형 언어 모델
- **LangChain**: LLM 애플리케이션 프레임워크
- **LangGraph**: 복잡한 에이전트 워크플로우 구축

### MCP (Model Context Protocol)
- **FastMCP**: 빠른 MCP 서버 구축 프레임워크
- **langchain-mcp-adapters**: LangChain과 MCP 통합
- **MultiServerMCPClient**: 여러 MCP 서버 관리

### 문서 처리 & 검색
- **PyMuPDFLoader**: PDF 파일 로딩
- **DirectoryLoader**: 디렉토리 기반 문서 일괄 로딩
- **RecursiveCharacterTextSplitter**: 텍스트 청킹
- **FAISS**: 고속 벡터 유사도 검색
- **OpenAI Embeddings**: 텍스트 임베딩 (`text-embedding-3-small`)

### 웹 검색
- **TavilySearch**: 실시간 뉴스 및 웹 검색

### 개발 도구
- **Jupyter Notebook**: 대화형 개발 환경
- **python-dotenv**: 환경 변수 관리
- **LangSmith**: LLM 애플리케이션 모니터링 및 디버깅

## 문제 해결 (Troubleshooting)

### 1. `ClosedResourceError` 발생

**증상**: `retrieve` 도구 실행 시 `Error: ClosedResourceError()` 발생

**원인**: `stdio_client` + `ClientSession`을 사용할 때 `async with` 블록이 끝나면 session이 자동으로 닫힘

**해결 방법**: `MultiServerMCPClient` 사용
```python
# ❌ 잘못된 방법
async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        tools = await load_mcp_tools(session)
# 블록이 끝나면 session 종료

# ✅ 올바른 방법
client = MultiServerMCPClient({
    "document-retriever": {
        "command": "../.venv/bin/python",
        "args": ["./mcp_server_rag.py"],
        "transport": "stdio",
    }
})
tools = await client.get_tools()  # session이 계속 유지됨
```

### 2. `OPENAI_BASE_URL` 관련 403 에러

**증상**: OpenAI Embeddings 사용 시 `PermissionDeniedError: 403 unauthorized`

**원인**: 시스템 환경변수에 `OPENAI_BASE_URL=https://api.fireworks.ai/...`가 설정됨

**해결 방법**:
```python
# mcp_server_rag.py에 이미 적용됨
if 'OPENAI_BASE_URL' in os.environ:
    del os.environ['OPENAI_BASE_URL']
```

### 3. `load_dotenv()` 실패

**증상**: `.env` 파일 로드 실패

**원인**: 작업 디렉토리가 `.env` 파일 위치와 다름

**해결 방법**:
```python
import os
os.chdir('/Users/ijunhyeong/Desktop/mcp/langgraph-mcp-agents/lee_mcp_tutorial')
load_dotenv(override=True)
```

### 4. Jupyter Kernel 선택 불가

**증상**: "langgraph-mcp" 커널이 목록에 없음

**해결 방법**:
```bash
source ../.venv/bin/activate
python -m ipykernel install --user --name=langgraph-mcp --display-name="Python (langgraph-mcp)"
```

### 5. Module Import 에러

**증상**: `ModuleNotFoundError: No module named 'utils'`

**원인**: Python 경로에 프로젝트 디렉토리가 없음

**해결 방법**:
```python
import sys
sys.path.insert(0, '/Users/ijunhyeong/Desktop/mcp/langgraph-mcp-agents/lee_mcp_tutorial')
```

## 학습 포인트

### 1. MCP Session 관리
- `stdio_client` + `ClientSession`: 블록 스코프 내에서만 유효
- `MultiServerMCPClient`: 전역적으로 session 유지
- Jupyter Notebook에서는 `MultiServerMCPClient` 권장

### 2. RAG 최적화
- 전역 변수로 retriever 캐싱
- 초기화는 첫 호출 시에만 수행
- stdio 모드에서는 `show_progress=False` 설정

### 3. 에이전트 프롬프팅
```python
prompt = (
    "You are a smart agent with multiple tools. "
    "Use `retrieve` tool to search information from iPhone documents. "
    "Use `tavily_search_results_json` tool to search recent news. "
    "Answer in English."
)
```
- 명확한 도구 사용 지침 제공
- 각 도구의 용도를 구체적으로 명시

### 4. 스트리밍 출력
- `astream_graph()` 함수로 실시간 출력
- `print_tool_info()` 함수로 도구 추적
- 색상 코딩으로 가독성 향상

## 참고 자료

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [Anthropic Claude](https://www.anthropic.com/claude)
- [LangChain](https://python.langchain.com/)
- [FAISS](https://github.com/facebookresearch/faiss)

## 라이선스

이 프로젝트는 학습 및 연구 목적으로 자유롭게 사용할 수 있습니다.

## 기여

버그 리포트, 기능 제안 및 Pull Request는 언제나 환영합니다!
