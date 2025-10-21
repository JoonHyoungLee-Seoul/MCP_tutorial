# Code Executor MCP 사용 가이드

## 개요

Code Executor MCP는 Python 코드를 실행하고 데이터 분석 및 시각화를 수행할 수 있는 강력한 도구입니다.

## 주요 기능

### 1. Python 코드 실행
- pandas, numpy, matplotlib 지원
- 데이터 분석 및 변환
- 수치 계산

### 2. 데이터 시각화
- 5가지 차트 타입 (line, bar, scatter, pie, hist)
- 고품질 이미지 생성 (300 DPI)
- 커스터마이징 가능한 제목, 레이블

### 3. 데이터 분석
- 통계 요약
- 그룹화 및 집계
- 정렬 및 필터링
- 상관관계 분석

### 4. 파일 처리
- CSV 읽기/쓰기
- JSON 데이터 처리

## MCP.ipynb에 통합하기

### 3개 MCP 서버 모두 통합

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.tools.tavily_search import TavilySearchResults
from utils import astream_graph

# 모델 초기화
model = ChatAnthropic(
    model_name="claude-3-7-sonnet-latest", temperature=0, max_tokens=20000
)

# 3개의 MCP 서버 통합
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
    "code-executor": {
        "command": "../.venv/bin/python",
        "args": ["./mcp_server_code_executor.py"],
        "transport": "stdio",
    },
})

# MCP 도구 로드
mcp_tools = await client.get_tools()

# TavilySearch 추가
tavily = TavilySearchResults(max_results=3, topic="news", days=3)

# 모든 도구 결합 (총 12개 도구!)
all_tools = mcp_tools + [tavily]

print(f"사용 가능한 도구: {len(all_tools)}개")
print([tool.name for tool in all_tools])

# 출력:
# 사용 가능한 도구: 12개
# ['retrieve',
#  'calculate', 'percentage_change', 'statistics_summary', 'currency_convert', 'compare_values',
#  'execute_python', 'create_visualization', 'analyze_data', 'read_csv', 'save_to_csv',
#  'tavily_search_results_json']

# 에이전트 생성
agent = create_react_agent(
    model,
    all_tools,
    prompt="""You are a powerful AI agent with multiple capabilities:

    - Document Retrieval: Use 'retrieve' to search iPhone documents
    - Web Search: Use 'tavily_search_results_json' for latest news
    - Calculations: Use calculator tools for math and statistics
    - Data Analysis: Use 'execute_python', 'analyze_data' for complex analysis
    - Visualization: Use 'create_visualization' to generate charts

    Choose the most appropriate tools based on the user's request.""",
    checkpointer=MemorySaver()
)

config = {"recursion_limit": 30, "thread_id": 1}
```

## 사용 예제

### 예제 1: 데이터 시각화 (기본)

```python
await astream_graph(
    agent,
    {
        "messages": """
        Create a bar chart showing iPhone sales:
        - iPhone 17: 11.4 million
        - iPhone 16: 10.0 million
        - iPhone 15: 8.5 million
        Save it as 'iphone_sales.png'
        """
    },
    config=config
)

# 출력:
# 🔧 Tool Selected: create_visualization
# ✅ Tool Executed: create_visualization
# Visualization created successfully!
# Chart Type:     bar
# Filename:       iphone_sales.png
# Location:       /path/to/output/iphone_sales.png
```

### 예제 2: 복잡한 데이터 분석

```python
await astream_graph(
    agent,
    {
        "messages": """
        Search for iPhone 17 sales data by region using tavily.
        Then create a JSON dataset and generate a pie chart showing market share.
        """
    },
    config=config
)

# 에이전트가 자동으로:
# 1. tavily_search_results_json으로 판매 데이터 검색
# 2. create_visualization으로 파이 차트 생성
```

### 예제 3: Python 코드 실행

```python
await astream_graph(
    agent,
    {
        "messages": """
        Use Python to analyze this data:
        Sales = [1000, 1200, 1500, 1800, 2000]

        Calculate:
        1. Mean and standard deviation
        2. Growth rate between first and last value
        3. Create a line plot showing the trend
        """
    },
    config=config
)

# 출력:
# 🔧 Tool Selected: execute_python
# ✅ Tool Executed: execute_python
# Code executed successfully!
# Output:
# Mean: 1500.0
# Std Dev: 387.3
# Growth: 100.0%
```

### 예제 4: 문서 + 계산 + 시각화 통합

```python
await astream_graph(
    agent,
    {
        "messages": """
        1. Retrieve iPhone 17 Pro and iPhone 16 Pro specifications from documents
        2. Extract screen sizes and battery capacities
        3. Calculate the percentage differences
        4. Create a comparison bar chart
        5. Save the data to CSV file
        """
    },
    config=config
)

# 에이전트가 자동으로:
# 1. retrieve (문서 검색)
# 2. percentage_change (증가율 계산)
# 3. create_visualization (차트 생성)
# 4. save_to_csv (CSV 저장)
```

### 예제 5: 웹 검색 + 데이터 분석 + 시각화

```python
await astream_graph(
    agent,
    {
        "messages": """
        Search for iPhone 17 pricing in different countries.
        Create a dataset with country names and prices.
        Generate a horizontal bar chart sorted by price.
        Also calculate statistical summary (mean, median, std dev).
        """
    },
    config=config
)

# 에이전트가 자동으로:
# 1. tavily_search_results_json (가격 검색)
# 2. analyze_data (통계 계산)
# 3. create_visualization (차트 생성)
```

### 예제 6: 복잡한 pandas 분석

```python
await astream_graph(
    agent,
    {
        "messages": """
        Execute Python code to analyze iPhone sales data:

        ```python
        import pandas as pd
        import matplotlib.pyplot as plt

        # Sample data
        data = {
            'Model': ['iPhone 17 Pro', 'iPhone 17', 'iPhone 16 Pro', 'iPhone 16'],
            'Q1_Sales': [2.5, 3.0, 2.0, 2.8],
            'Q2_Sales': [2.8, 3.2, 2.2, 3.0],
            'Q3_Sales': [3.0, 3.5, 2.5, 3.2]
        }

        df = pd.DataFrame(data)
        df['Total'] = df[['Q1_Sales', 'Q2_Sales', 'Q3_Sales']].sum(axis=1)
        df['Average'] = df['Total'] / 3

        print(df)

        # Create visualization
        df.plot(x='Model', y=['Q1_Sales', 'Q2_Sales', 'Q3_Sales'], kind='bar')
        plt.title('Quarterly iPhone Sales (Millions)')
        plt.ylabel('Sales (Millions)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('output/quarterly_sales.png')
        ```
        """
    },
    config=config
)
```

## Code Executor MCP 도구 목록

### 1. `execute_python(code: str)`
Python 코드를 안전하게 실행합니다.

**지원 라이브러리:**
- pandas (데이터 분석)
- numpy (수치 계산)
- matplotlib (시각화)
- json, math, datetime, collections

**예제:**
```python
code = """
import pandas as pd
df = pd.DataFrame({
    'Product': ['iPhone 17', 'iPhone 16'],
    'Price': [1199, 999]
})
print(df)
print(f"Average price: ${df['Price'].mean()}")
"""
```

### 2. `create_visualization(data, chart_type, title, x_label, y_label, filename)`
데이터 시각화 차트를 생성합니다.

**차트 타입:**
- `line`: 선 그래프
- `bar`: 막대 그래프
- `scatter`: 산점도
- `pie`: 파이 차트
- `hist`: 히스토그램

**데이터 형식:**
```json
{
    "x": [1, 2, 3, 4],
    "y": [10, 20, 15, 25]
}
```

또는 파이 차트용:
```json
{
    "labels": ["iPhone 17", "iPhone 16", "iPhone 15"],
    "values": [45, 30, 25]
}
```

### 3. `analyze_data(data, operation)`
pandas를 사용한 데이터 분석

**지원 작업:**
- `describe`: 통계 요약
- `groupby:column`: 그룹화 및 집계
- `sort:column`: 정렬
- `correlation`: 상관관계 분석

**데이터 형식:**
```json
[
    {"product": "iPhone 17", "sales": 1000, "region": "US"},
    {"product": "iPhone 16", "sales": 800, "region": "US"}
]
```

### 4. `read_csv(filename)`
CSV 파일 읽기

### 5. `save_to_csv(data, filename)`
데이터를 CSV로 저장

## 실전 시나리오

### 시나리오 1: 완전한 분석 파이프라인

```python
query = """
Step 1: Search for iPhone 17 sales data in different regions using web search
Step 2: Create a JSON dataset from the search results
Step 3: Save the data to 'iphone_sales.csv'
Step 4: Analyze the data to get statistical summary
Step 5: Create a bar chart showing sales by region
Step 6: Calculate which region has the highest growth compared to iPhone 16
"""

await astream_graph(agent, {"messages": query}, config=config)
```

### 시나리오 2: 문서 기반 비교 분석

```python
query = """
1. Retrieve iPhone 17 Pro specifications from documents
2. Extract all numeric specifications (screen size, battery, camera MP, etc.)
3. Compare with iPhone 16 Pro specifications
4. Create a comparison table using pandas
5. Generate a radar chart showing the differences
6. Save results to 'comparison.csv'
"""

await astream_graph(agent, {"messages": query}, config=config)
```

### 시나리오 3: 트렌드 분석

```python
query = """
Using web search, find iPhone sales numbers for the past 5 generations.
Then:
1. Create a time series visualization
2. Calculate year-over-year growth rates
3. Perform linear regression to predict next year's sales
4. Generate a forecast chart with confidence intervals
"""

await astream_graph(agent, {"messages": query}, config=config)
```

## 생성된 파일 확인

모든 생성된 파일은 `output/` 디렉토리에 저장됩니다:

```bash
ls -la output/

# 출력 예시:
# iphone_sales.png       - 판매 차트
# quarterly_sales.png    - 분기별 분석
# comparison.csv         - 비교 데이터
# market_share.png       - 시장 점유율 파이 차트
```

## 보안 및 제한사항

### ✅ 허용되는 것
- pandas, numpy, matplotlib 사용
- 수학 계산 및 통계 분석
- output/ 디렉토리에 파일 저장
- JSON 데이터 처리

### ❌ 제한되는 것
- 파일 시스템 접근 (output/ 외부)
- subprocess, os.system 호출
- 네트워크 요청
- 임의의 모듈 import

## 장점

✅ **강력한 분석**: pandas와 numpy로 복잡한 데이터 분석
✅ **시각화**: 고품질 차트 자동 생성
✅ **자동화**: 여러 단계의 분석을 한 번에 실행
✅ **통합성**: 다른 MCP 도구들과 완벽한 연동
✅ **안전성**: 샌드박스 환경에서 안전하게 실행

## 다음 단계

Code Executor를 활용하여:
- 복잡한 데이터 분석 자동화
- 커스텀 리포트 생성
- 실시간 데이터 모니터링
- ML 모델 예측 (scikit-learn 추가 가능)

## 추가 라이브러리 설치

더 강력한 기능이 필요하다면:

```bash
pip install scikit-learn seaborn plotly
```

그리고 `mcp_server_code_executor.py`의 safe_globals에 추가하세요!
