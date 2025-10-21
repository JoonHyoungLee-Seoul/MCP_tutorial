# MCP.ipynb에 추가할 예제 셀

## 새로운 Cell 추가: 3개 MCP 서버 통합

```python
# Cell: 3개 MCP 서버 모두 통합
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.runnables import RunnableConfig
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

# 모든 도구 결합
all_tools = mcp_tools + [tavily]

print(f"\n{'='*60}")
print(f"🎉 통합 완료! 사용 가능한 도구: {len(all_tools)}개")
print(f"{'='*60}\n")

for i, tool in enumerate(all_tools, 1):
    category = ""
    if tool.name == "retrieve":
        category = "📚 Document"
    elif tool.name in ["calculate", "percentage_change", "statistics_summary", "currency_convert", "compare_values"]:
        category = "🧮 Calculator"
    elif tool.name in ["execute_python", "create_visualization", "analyze_data", "read_csv", "save_to_csv"]:
        category = "💻 Code Executor"
    elif tool.name == "tavily_search_results_json":
        category = "🔍 Web Search"

    print(f"{i:2d}. {category:20s} {tool.name}")

print(f"\n{'='*60}\n")

# 에이전트 생성
agent = create_react_agent(
    model,
    all_tools,
    prompt="""You are a powerful AI agent with multiple capabilities:

    📚 Document Retrieval (retrieve):
       - Search information from iPhone technical documents

    🧮 Calculator (calculate, percentage_change, statistics_summary, currency_convert, compare_values):
       - Perform mathematical calculations and statistical analysis

    💻 Code Executor (execute_python, create_visualization, analyze_data, read_csv, save_to_csv):
       - Execute Python code for data analysis
       - Create visualizations (charts, graphs)
       - Process and save data files

    🔍 Web Search (tavily_search_results_json):
       - Search latest news and web information

    Choose the most appropriate tools based on the user's request.
    You can use multiple tools in sequence for complex tasks.
    Always explain which tools you're using and why.""",
    checkpointer=MemorySaver()
)

# 설정
config = RunnableConfig(recursion_limit=30, thread_id=1)

print("✅ Agent created successfully!")
```

## 테스트 예제 1: 간단한 시각화

```python
# Cell: 테스트 1 - 기본 차트 생성
await astream_graph(
    agent,
    {
        "messages": """
        Create a bar chart showing iPhone sales:
        - iPhone 17 Pro: 2.8 million
        - iPhone 17: 3.5 million
        - iPhone 16 Pro: 2.5 million
        - iPhone 16: 3.2 million

        Title: "iPhone Sales Comparison (Q3 2025)"
        Save as: sales_comparison.png
        """
    },
    config=config
)
```

## 테스트 예제 2: 문서 검색 + 계산

```python
# Cell: 테스트 2 - 문서 검색 + 가격 계산
await astream_graph(
    agent,
    {
        "messages": """
        1. Retrieve iPhone 17 Pro price from documents
        2. Convert the USD price to KRW using exchange rate 1,300
        3. Show the result
        """
    },
    config=config
)
```

## 테스트 예제 3: 웹 검색 + 데이터 분석

```python
# Cell: 테스트 3 - 웹 검색 + 통계 분석
await astream_graph(
    agent,
    {
        "messages": """
        1. Search for iPhone 17 sales data using web search
        2. Extract sales numbers from the search results
        3. Calculate statistical summary (mean, median, std dev)
        4. Create a visualization showing the trend
        """
    },
    config=config
)
```

## 테스트 예제 4: 복합 분석 (모든 도구 사용)

```python
# Cell: 테스트 4 - 종합 분석
await astream_graph(
    agent,
    {
        "messages": """
        Complete analysis task:

        Step 1: Retrieve iPhone 17 and iPhone 16 battery capacity from documents
        Step 2: Calculate the percentage difference
        Step 3: Search for battery life comparison reviews on the web
        Step 4: Create a comparison chart showing:
           - Battery capacity (mAh)
           - Percentage difference
        Step 5: Save the data to battery_comparison.csv
        Step 6: Execute Python code to analyze which model has better efficiency
        """
    },
    config=config
)
```

## 테스트 예제 5: Python 코드 실행

```python
# Cell: 테스트 5 - Python 코드 실행
await astream_graph(
    agent,
    {
        "messages": """
        Execute this Python code:

        ```python
        import pandas as pd
        import matplotlib.pyplot as plt
        import numpy as np

        # iPhone sales data
        models = ['iPhone 17 Pro', 'iPhone 17', 'iPhone 16 Pro', 'iPhone 16']
        sales_q1 = [2.5, 3.0, 2.0, 2.8]
        sales_q2 = [2.8, 3.2, 2.2, 3.0]
        sales_q3 = [3.0, 3.5, 2.5, 3.2]

        # Create DataFrame
        df = pd.DataFrame({
            'Model': models,
            'Q1': sales_q1,
            'Q2': sales_q2,
            'Q3': sales_q3
        })

        # Calculate totals and averages
        df['Total'] = df[['Q1', 'Q2', 'Q3']].sum(axis=1)
        df['Average'] = df['Total'] / 3
        df['Growth'] = ((df['Q3'] - df['Q1']) / df['Q1'] * 100).round(2)

        print("Sales Analysis Results:")
        print("=" * 70)
        print(df.to_string(index=False))
        print("=" * 70)

        # Find best performing model
        best_model = df.loc[df['Total'].idxmax(), 'Model']
        best_growth = df.loc[df['Growth'].idxmax(), 'Model']

        print(f"\\nBest selling model: {best_model}")
        print(f"Highest growth model: {best_growth}")

        # Create visualization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Quarterly sales
        x = np.arange(len(models))
        width = 0.25

        ax1.bar(x - width, sales_q1, width, label='Q1', alpha=0.8)
        ax1.bar(x, sales_q2, width, label='Q2', alpha=0.8)
        ax1.bar(x + width, sales_q3, width, label='Q3', alpha=0.8)

        ax1.set_xlabel('Model')
        ax1.set_ylabel('Sales (Millions)')
        ax1.set_title('Quarterly iPhone Sales')
        ax1.set_xticks(x)
        ax1.set_xticklabels(models, rotation=45, ha='right')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Total sales pie chart
        ax2.pie(df['Total'], labels=models, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Market Share (Total Sales)')

        plt.tight_layout()
        plt.savefig('output/sales_analysis.png', dpi=300, bbox_inches='tight')

        print("\\n✅ Chart saved: output/sales_analysis.png")
        ```
        """
    },
    config=config
)
```

## 테스트 예제 6: 실시간 데이터 분석

```python
# Cell: 테스트 6 - 실시간 뉴스 + 데이터 분석
await astream_graph(
    agent,
    {
        "messages": """
        Research and Analysis Task:

        1. Search for latest iPhone 17 sales reports using web search
        2. Extract key sales numbers and dates
        3. Create a JSON dataset with the information
        4. Analyze the data to calculate:
           - Total sales across all regions
           - Average daily sales
           - Growth rate compared to iPhone 16
        5. Create a timeline visualization
        6. Save results to sales_report.csv
        7. Generate a summary report
        """
    },
    config=config
)
```

## 테스트 예제 7: 사양 비교 분석

```python
# Cell: 테스트 7 - 상세 사양 비교
await astream_graph(
    agent,
    {
        "messages": """
        Detailed Specification Comparison:

        1. Retrieve ALL technical specifications for iPhone 17 Pro from documents:
           - Display (size, resolution, brightness)
           - Camera (megapixels, features)
           - Battery (capacity, life)
           - Processor (chip name, cores)
           - Storage options
           - Colors available

        2. Use calculator to compute:
           - Screen PPI (pixels per inch)
           - Battery capacity increase from iPhone 16
           - Price per GB for each storage option

        3. Create visualizations:
           - Radar chart for key specs
           - Bar chart for storage pricing
           - Pie chart for color options popularity (if data available)

        4. Save all data to specs_comparison.csv
        """
    },
    config=config
)
```

## 출력 파일 확인

```python
# Cell: 생성된 파일 확인
import os

output_dir = "./output"
if os.path.exists(output_dir):
    files = os.listdir(output_dir)
    print(f"\n{'='*60}")
    print(f"📁 Generated Files in output/ directory:")
    print(f"{'='*60}\n")

    for file in sorted(files):
        filepath = os.path.join(output_dir, file)
        size = os.path.getsize(filepath)

        # File type icon
        icon = "📊" if file.endswith('.png') else "📄"

        print(f"{icon} {file:40s} ({size:,} bytes)")

    print(f"\n{'='*60}")
    print(f"Total: {len(files)} files")
    print(f"{'='*60}\n")
else:
    print("No output directory found yet. Run some examples to generate files!")
```

## 이미지 표시 (Jupyter Notebook)

```python
# Cell: 생성된 차트 이미지 표시
from IPython.display import Image, display
import os

output_dir = "./output"

# 모든 PNG 파일 표시
png_files = [f for f in os.listdir(output_dir) if f.endswith('.png')]

for png_file in sorted(png_files):
    print(f"\n{'='*60}")
    print(f"📊 {png_file}")
    print(f"{'='*60}\n")
    display(Image(filename=os.path.join(output_dir, png_file)))
```

## 성능 테스트

```python
# Cell: 도구 응답 시간 측정
import time

test_queries = [
    ("Calculator", "Calculate 1199 * 1300"),
    ("Retriever", "What are the color options for iPhone 17 Pro?"),
    ("Visualization", "Create a simple line chart with data: x=[1,2,3], y=[4,5,6]"),
]

results = []

for tool_name, query in test_queries:
    print(f"\nTesting {tool_name}...")
    start = time.time()

    result = await astream_graph(
        agent,
        {"messages": query},
        config={"recursion_limit": 30, "thread_id": int(time.time())}
    )

    duration = time.time() - start
    results.append((tool_name, duration))
    print(f"✅ Completed in {duration:.2f} seconds")

print(f"\n{'='*60}")
print("Performance Summary:")
print(f"{'='*60}\n")

for tool_name, duration in results:
    print(f"{tool_name:20s} {duration:6.2f}s")

print(f"\n{'='*60}")
```

## 사용 팁

### 💡 Tip 1: 복잡한 작업은 단계별로 명시
```python
# ✅ Good
"1. Retrieve data\n2. Calculate\n3. Visualize"

# ❌ Bad
"Do everything about iPhone sales"
```

### 💡 Tip 2: 파일명 지정
```python
# ✅ Good
"Save as 'sales_2025_q3.png'"

# ❌ Bad
"Save the chart"  # 기본 파일명 사용
```

### 💡 Tip 3: 데이터 형식 명시
```python
# ✅ Good
"Create JSON: [{'name': 'iPhone 17', 'price': 1199}]"

# ❌ Bad
"Create some data"
```
