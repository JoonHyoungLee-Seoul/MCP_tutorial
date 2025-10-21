# Calculator MCP 사용 가이드

## 설치 및 설정

Calculator MCP 서버가 `mcp_server_calculator.py`로 생성되었습니다.

## MCP.ipynb에 통합하기

### 방법 1: Calculator만 추가

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from utils import astream_graph

# 모델 초기화
model = ChatAnthropic(
    model_name="claude-3-7-sonnet-latest", temperature=0, max_tokens=20000
)

# 3개의 MCP 서버 통합: RAG + Calculator
client = MultiServerMCPClient({
    "document-retriever": {
        "command": "../.venv/bin/python",
        "args": ["./mcp_server_rag.py"],
        "transport": "stdio",
    },
    "calculator": {
        "command": "../.venv/bin/python",
        "args": ["./mcp_server_calculator.py"],
        "transport": "stdio",
    },
})

# MCP 도구 로드
mcp_tools = await client.get_tools()

# TavilySearch 추가
from langchain_community.tools.tavily_search import TavilySearchResults
tavily = TavilySearchResults(max_results=3, topic="news", days=3)

# 모든 도구 결합
all_tools = mcp_tools + [tavily]

print(f"사용 가능한 도구: {[tool.name for tool in all_tools]}")
# 출력: ['retrieve', 'calculate', 'percentage_change', 'statistics_summary',
#        'currency_convert', 'compare_values', 'tavily_search_results_json']

# 에이전트 생성
agent = create_react_agent(
    model,
    all_tools,
    prompt="You have access to document retrieval, calculator, and web search tools. Use them wisely.",
    checkpointer=MemorySaver()
)
```

## 사용 예제

### 예제 1: 가격 계산
```python
await astream_graph(
    agent,
    {"messages": "iPhone 17 Pro 가격이 $1,199인데, 환율이 1,300원일 때 한화로 얼마야?"},
    config={"recursion_limit": 30, "thread_id": 1}
)

# 출력:
# 🔧 Tool Selected: currency_convert
# ✅ Tool Executed: currency_convert
# Currency Conversion:
# Amount:         1,199.00 USD
# Exchange Rate:  1 USD = 1,300.0000 KRW
# Result:         1,558,700.00 KRW
```

### 예제 2: 사양 비교
```python
await astream_graph(
    agent,
    {
        "messages": (
            "Retrieve iPhone 17 Pro and iPhone 16 Pro battery capacity from documents. "
            "Then compare the two values and show the percentage difference."
        )
    },
    config={"recursion_limit": 30, "thread_id": 2}
)

# 에이전트가 자동으로:
# 1. retrieve 도구로 문서에서 배터리 용량 검색
# 2. compare_values 도구로 비교 분석
```

### 예제 3: 통계 분석
```python
await astream_graph(
    agent,
    {
        "messages": (
            "Search for iPhone 17 sales numbers in different regions using tavily. "
            "Then calculate the statistical summary (mean, median, std dev)."
        )
    },
    config={"recursion_limit": 30, "thread_id": 3}
)

# 에이전트가 자동으로:
# 1. tavily_search_results_json으로 판매 데이터 검색
# 2. statistics_summary 도구로 통계 계산
```

### 예제 4: 복잡한 계산
```python
await astream_graph(
    agent,
    {"messages": "Calculate the area of iPhone 17 Pro screen if width is 71.5mm and height is 154.3mm. Answer in square centimeters."},
    config={"recursion_limit": 30, "thread_id": 4}
)

# 출력:
# 🔧 Tool Selected: calculate
# ✅ Tool Executed: calculate
# Result: 110.32 square centimeters
```

### 예제 5: 증가율 계산
```python
await astream_graph(
    agent,
    {"messages": "iPhone 16 Pro sold 10 million units, iPhone 17 Pro sold 11.4 million. What's the percentage increase?"},
    config={"recursion_limit": 30, "thread_id": 5}
)

# 출력:
# 🔧 Tool Selected: percentage_change
# ✅ Tool Executed: percentage_change
# Increase of 14.00% (from 10000000.0 to 11400000.0)
```

## Calculator MCP 도구 목록

### 1. `calculate(expression: str)`
- 수학 표현식 계산
- 지원: +, -, *, /, sqrt(), sin(), cos(), log(), pi, e

### 2. `percentage_change(old_value: float, new_value: float)`
- 두 값 사이의 증가/감소율 계산

### 3. `statistics_summary(numbers: str)`
- 통계 요약 (평균, 중앙값, 표준편차, 최소/최대)

### 4. `currency_convert(amount: float, from_currency: str, to_currency: str, exchange_rate: float)`
- 환율 계산

### 5. `compare_values(value1: float, value2: float, unit: str)`
- 두 값 비교 및 차이 계산

## 실전 시나리오

### 시나리오 1: 제품 분석
```python
query = """
1. Retrieve iPhone 17 Pro specifications from documents
2. Calculate the screen-to-body ratio if screen is 6.3 inch diagonal and body is 146.6mm x 70.6mm
3. Compare with iPhone 16 Pro's 6.1 inch screen
4. Show percentage difference
"""

await astream_graph(agent, {"messages": query}, config=config)
```

### 시나리오 2: 가격 분석
```python
query = """
1. Search for iPhone 17 pricing in different countries using tavily
2. Convert all prices to USD
3. Calculate statistical summary
4. Show which country has the best price
"""

await astream_graph(agent, {"messages": query}, config=config)
```

### 시나리오 3: 판매 트렌드 분석
```python
query = """
1. Search for iPhone 17 weekly sales data using tavily
2. Calculate the average sales per week
3. Compare with iPhone 16 sales from documents
4. Show percentage growth trend
"""

await astream_graph(agent, {"messages": query}, config=config)
```

## 장점

✅ **정확한 계산**: Python의 math 라이브러리 사용으로 정확성 보장
✅ **다양한 기능**: 기본 계산부터 통계, 환율까지
✅ **에러 처리**: 잘못된 입력에 대한 명확한 에러 메시지
✅ **포맷팅**: 읽기 쉬운 출력 형식
✅ **통합성**: 다른 MCP 도구들과 완벽하게 연동

## 다음 단계

더 고급 기능이 필요하다면:
- Code Executor MCP: pandas, numpy, matplotlib 사용
- Database MCP: 계산 결과를 데이터베이스에 저장
- Visualization MCP: 그래프 및 차트 생성
