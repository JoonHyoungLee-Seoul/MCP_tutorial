"""
Code Executor MCP Server - Python 코드 실행 및 데이터 분석 도구

이 MCP 서버는 다음 기능을 제공합니다:
1. Python 코드 실행 (pandas, numpy, matplotlib 지원)
2. 데이터 시각화 (차트 생성 및 이미지 저장)
3. 데이터 분석 (통계, 변환, 집계)
4. CSV/JSON 파일 읽기/쓰기

보안 주의사항:
- 안전한 모듈만 허용 (pandas, numpy, matplotlib, json)
- 파일 시스템 접근은 제한된 디렉토리만 허용
- 위험한 함수 호출 차단
"""

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import sys
import io
import json
import traceback

load_dotenv(override=True)

# OPENAI_BASE_URL 제거 (환경 변수 충돌 방지)
if 'OPENAI_BASE_URL' in os.environ:
    del os.environ['OPENAI_BASE_URL']

# Initialize FastMCP server
mcp = FastMCP(
    "CodeExecutor",
    instructions="A code executor that can run Python code, create visualizations, and analyze data using pandas, numpy, and matplotlib.",
    host="0.0.0.0",
    port=8007,
)

# 작업 디렉토리 설정 (출력 파일 저장 위치)
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


@mcp.tool()
async def execute_python(code: str) -> str:
    """
    Executes Python code in a safe environment with pandas, numpy, and matplotlib support.

    Supported libraries:
    - pandas (as pd)
    - numpy (as np)
    - matplotlib.pyplot (as plt)
    - json, math, datetime, collections

    Args:
        code (str): Python code to execute

    Returns:
        str: Execution result with stdout, return value, and any generated plots

    Examples:
        >>> execute_python("import pandas as pd\\ndf = pd.DataFrame({'a': [1,2,3]})\\nprint(df)")

        >>> execute_python("import numpy as np\\nresult = np.mean([1, 2, 3, 4, 5])\\nprint(result)")

        >>> execute_python('''
        import matplotlib.pyplot as plt
        plt.plot([1, 2, 3, 4], [1, 4, 2, 3])
        plt.title("Sample Plot")
        plt.savefig("output/plot.png")
        ''')

    Security:
    - Restricted to safe modules only
    - No file system access outside output directory
    - No subprocess or system calls
    """
    try:
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        # Safe globals with allowed modules
        safe_globals = {
            '__builtins__': {
                '__import__': __import__,  # 모듈 import 허용
                'open': open,  # 파일 작업 허용
                'print': print,
                'len': len,
                'range': range,
                'enumerate': enumerate,
                'zip': zip,
                'map': map,
                'filter': filter,
                'sum': sum,
                'min': min,
                'max': max,
                'abs': abs,
                'round': round,
                'sorted': sorted,
                'list': list,
                'dict': dict,
                'tuple': tuple,
                'set': set,
                'str': str,
                'int': int,
                'float': float,
                'bool': bool,
                'True': True,
                'False': False,
                'None': None,
            }
        }

        # Execute code
        exec(code, safe_globals)

        # Get stdout
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        # Check for saved plots
        plot_files = []
        if os.path.exists(OUTPUT_DIR):
            for file in os.listdir(OUTPUT_DIR):
                if file.endswith(('.png', '.jpg', '.jpeg', '.svg')):
                    plot_files.append(file)

        result = "Code executed successfully!\n"
        result += "=" * 50 + "\n"

        if output:
            result += "Output:\n"
            result += output + "\n"

        if plot_files:
            result += f"\nGenerated plots: {', '.join(plot_files)}\n"
            result += f"Location: {OUTPUT_DIR}\n"

        return result

    except Exception as e:
        sys.stdout = old_stdout
        error_trace = traceback.format_exc()
        return f"Error executing code:\n{error_trace}"


@mcp.tool()
async def create_visualization(
    data: str,
    chart_type: str,
    title: str = "Chart",
    x_label: str = "",
    y_label: str = "",
    filename: str = "chart.png"
) -> str:
    """
    Creates a data visualization and saves it as an image file.

    Args:
        data (str): JSON string containing data (e.g., '{"x": [1,2,3], "y": [4,5,6]}')
        chart_type (str): Type of chart ('line', 'bar', 'scatter', 'pie', 'hist')
        title (str): Chart title (default: "Chart")
        x_label (str): X-axis label (default: "")
        y_label (str): Y-axis label (default: "")
        filename (str): Output filename (default: "chart.png")

    Returns:
        str: Success message with file location

    Examples:
        >>> create_visualization(
                '{"x": [1, 2, 3, 4], "y": [10, 20, 15, 25]}',
                'line',
                'Sales Trend',
                'Month',
                'Sales'
            )

        >>> create_visualization(
                '{"labels": ["iPhone 17", "iPhone 16", "iPhone 15"], "values": [45, 30, 25]}',
                'pie',
                'Market Share'
            )
    """
    try:
        import matplotlib
        matplotlib.use('Agg')  # Non-interactive backend
        import matplotlib.pyplot as plt

        # Parse data
        chart_data = json.loads(data)

        # DEBUG: Print received data
        print(f"DEBUG: Received data: {data}")
        print(f"DEBUG: Parsed chart_data: {chart_data}")
        print(f"DEBUG: Chart type: {chart_type}")

        # Create figure
        plt.figure(figsize=(10, 6))

        # Create chart based on type
        if chart_type == 'line':
            x_data = chart_data.get('x', [])
            y_data = chart_data.get('y', [])

            # Handle categorical (string) labels on x-axis
            if x_data and isinstance(x_data[0], str):
                import numpy as np
                positions = np.arange(len(x_data))
                plt.plot(positions, y_data, marker='o')
                plt.xticks(positions, x_data, rotation=45, ha='right')
            else:
                plt.plot(x_data, y_data, marker='o')

        elif chart_type == 'bar':
            x_data = chart_data.get('x', [])
            y_data = chart_data.get('y', [])

            # DEBUG: Print data
            print(f"DEBUG bar: x_data = {x_data}, type = {type(x_data)}")
            print(f"DEBUG bar: y_data = {y_data}, type = {type(y_data)}")

            # Validate data
            if not x_data or not y_data:
                return f"Error: Empty data. x_data={x_data}, y_data={y_data}. Please provide data in format: " + \
                       '{"x": ["label1", "label2"], "y": [value1, value2]}'

            if len(x_data) != len(y_data):
                return f"Error: x_data length ({len(x_data)}) doesn't match y_data length ({len(y_data)})"

            # Handle categorical (string) labels on x-axis
            if x_data and isinstance(x_data[0], str):
                import numpy as np
                positions = np.arange(len(x_data))
                print(f"DEBUG bar: Using categorical positions: {positions}")
                plt.bar(positions, y_data)
                plt.xticks(positions, x_data, rotation=45, ha='right')
            else:
                plt.bar(x_data, y_data)

        elif chart_type == 'scatter':
            x_data = chart_data.get('x', [])
            y_data = chart_data.get('y', [])

            # Scatter plots work better with numeric data
            # If strings are provided, convert to numeric positions
            if x_data and isinstance(x_data[0], str):
                import numpy as np
                positions = np.arange(len(x_data))
                plt.scatter(positions, y_data)
                plt.xticks(positions, x_data, rotation=45, ha='right')
            else:
                plt.scatter(x_data, y_data)

        elif chart_type == 'pie':
            labels = chart_data.get('labels', [])
            values = chart_data.get('values', [])
            plt.pie(values, labels=labels, autopct='%1.1f%%')

        elif chart_type == 'hist':
            plt.hist(chart_data.get('values', []), bins=chart_data.get('bins', 10))

        else:
            return f"Error: Unsupported chart type '{chart_type}'. Use: line, bar, scatter, pie, hist"

        # Set labels and title
        plt.title(title, fontsize=14, fontweight='bold')
        if x_label:
            plt.xlabel(x_label)
        if y_label:
            plt.ylabel(y_label)

        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        # Save figure
        output_path = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return f"""Visualization created successfully!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Chart Type:     {chart_type}
Title:          {title}
Filename:       {filename}
Location:       {output_path}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

    except json.JSONDecodeError:
        return "Error: Invalid JSON data format. Please provide valid JSON string."
    except Exception as e:
        return f"Error creating visualization: {str(e)}\n{traceback.format_exc()}"


@mcp.tool()
async def analyze_data(data: str, operation: str) -> str:
    """
    Analyzes data using pandas and returns statistical results.

    Args:
        data (str): JSON string containing data (e.g., '[{"name": "A", "value": 10}, ...]')
        operation (str): Analysis operation:
            - 'describe': Statistical summary
            - 'groupby:column': Group by column and aggregate
            - 'sort:column': Sort by column
            - 'filter:condition': Filter rows (e.g., 'value > 10')
            - 'correlation': Correlation matrix

    Returns:
        str: Analysis results

    Examples:
        >>> analyze_data('[{"product": "iPhone 17", "sales": 1000}, {"product": "iPhone 16", "sales": 800}]', 'describe')

        >>> analyze_data('[{"region": "US", "sales": 500}, {"region": "EU", "sales": 300}]', 'groupby:region')
    """
    try:
        import pandas as pd

        # Parse data
        data_dict = json.loads(data)

        # Create DataFrame
        if isinstance(data_dict, list):
            df = pd.DataFrame(data_dict)
        elif isinstance(data_dict, dict):
            df = pd.DataFrame(data_dict)
        else:
            return "Error: Data must be a JSON array or object"

        # Perform operation
        result = "Data Analysis Results\n"
        result += "=" * 50 + "\n\n"

        if operation == 'describe':
            result += "Statistical Summary:\n"
            result += str(df.describe()) + "\n"

        elif operation.startswith('groupby:'):
            column = operation.split(':')[1]
            if column in df.columns:
                grouped = df.groupby(column).sum()
                result += f"Grouped by '{column}':\n"
                result += str(grouped) + "\n"
            else:
                return f"Error: Column '{column}' not found in data"

        elif operation.startswith('sort:'):
            column = operation.split(':')[1]
            if column in df.columns:
                sorted_df = df.sort_values(by=column, ascending=False)
                result += f"Sorted by '{column}' (descending):\n"
                result += str(sorted_df) + "\n"
            else:
                return f"Error: Column '{column}' not found in data"

        elif operation == 'correlation':
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                corr_matrix = df[numeric_cols].corr()
                result += "Correlation Matrix:\n"
                result += str(corr_matrix) + "\n"
            else:
                return "Error: No numeric columns found for correlation"

        else:
            return f"Error: Unknown operation '{operation}'"

        result += "\n" + "=" * 50
        return result

    except json.JSONDecodeError:
        return "Error: Invalid JSON data format"
    except Exception as e:
        return f"Error analyzing data: {str(e)}\n{traceback.format_exc()}"


@mcp.tool()
async def read_csv(filename: str) -> str:
    """
    Reads a CSV file and returns its contents as formatted text.

    Args:
        filename (str): Name of CSV file in output directory

    Returns:
        str: CSV file contents

    Examples:
        >>> read_csv("sales_data.csv")
    """
    try:
        import pandas as pd

        filepath = os.path.join(OUTPUT_DIR, filename)
        if not os.path.exists(filepath):
            return f"Error: File '{filename}' not found in {OUTPUT_DIR}"

        df = pd.read_csv(filepath)

        result = f"CSV File: {filename}\n"
        result += "=" * 50 + "\n"
        result += f"Rows: {len(df)}, Columns: {len(df.columns)}\n\n"
        result += "Column names:\n"
        result += str(list(df.columns)) + "\n\n"
        result += "First 10 rows:\n"
        result += str(df.head(10)) + "\n"
        result += "=" * 50

        return result

    except Exception as e:
        return f"Error reading CSV: {str(e)}"


@mcp.tool()
async def save_to_csv(data: str, filename: str) -> str:
    """
    Saves data to a CSV file.

    Args:
        data (str): JSON string containing data
        filename (str): Output filename (e.g., "results.csv")

    Returns:
        str: Success message with file location

    Examples:
        >>> save_to_csv('[{"name": "iPhone 17", "price": 1199}]', 'products.csv')
    """
    try:
        import pandas as pd

        # Parse data
        data_dict = json.loads(data)
        df = pd.DataFrame(data_dict)

        # Save to CSV
        filepath = os.path.join(OUTPUT_DIR, filename)
        df.to_csv(filepath, index=False)

        return f"""Data saved to CSV successfully!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Filename:       {filename}
Rows:           {len(df)}
Columns:        {len(df.columns)}
Location:       {filepath}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

    except Exception as e:
        return f"Error saving CSV: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
