"""
Calculator MCP Server - 수학 계산 및 통계 분석 도구

이 MCP 서버는 다음 기능을 제공합니다:
1. 기본 계산 (사칙연산)
2. 고급 수학 함수 (삼각함수, 로그, 지수)
3. 통계 계산 (평균, 중앙값, 표준편차)
4. 퍼센트 계산 (증가율, 감소율)
5. 환율 계산
"""

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import math
import statistics

load_dotenv(override=True)

# Initialize FastMCP server
mcp = FastMCP(
    "Calculator",
    instructions="A calculator that can perform mathematical calculations, statistics, and currency conversions.",
    host="0.0.0.0",
    port=8006,
)


@mcp.tool()
async def calculate(expression: str) -> str:
    """
    Evaluates a mathematical expression and returns the result.

    Supports:
    - Basic operations: +, -, *, /, //, %, **
    - Functions: sqrt(), sin(), cos(), tan(), log(), exp(), abs()
    - Constants: pi, e

    Args:
        expression (str): Mathematical expression to evaluate (e.g., "2 + 3 * 4", "sqrt(16)", "sin(pi/2)")

    Returns:
        str: Calculation result

    Examples:
        >>> calculate("1199 * 1300")
        "1558700"

        >>> calculate("sqrt(144) + 10")
        "22.0"

        >>> calculate("(1199 - 999) / 999 * 100")
        "20.02002002002002"
    """
    try:
        # Safe math functions
        safe_dict = {
            'abs': abs,
            'round': round,
            'sqrt': math.sqrt,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log,
            'log10': math.log10,
            'exp': math.exp,
            'pow': pow,
            'pi': math.pi,
            'e': math.e,
        }

        # Evaluate expression
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        return f"Result: {result}"

    except Exception as e:
        return f"Error: {str(e)}\nPlease check your expression format."


@mcp.tool()
async def percentage_change(old_value: float, new_value: float) -> str:
    """
    Calculates the percentage change between two values.

    Args:
        old_value (float): Original value
        new_value (float): New value

    Returns:
        str: Percentage change with explanation

    Examples:
        >>> percentage_change(1000, 1200)
        "Increase of 20.0%"

        >>> percentage_change(1200, 1000)
        "Decrease of 16.67%"
    """
    try:
        if old_value == 0:
            return "Error: Cannot calculate percentage change from zero."

        change = ((new_value - old_value) / old_value) * 100

        if change > 0:
            return f"Increase of {change:.2f}% (from {old_value} to {new_value})"
        elif change < 0:
            return f"Decrease of {abs(change):.2f}% (from {old_value} to {new_value})"
        else:
            return f"No change (both values are {old_value})"

    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def statistics_summary(numbers: str) -> str:
    """
    Calculates statistical summary for a list of numbers.

    Args:
        numbers (str): Comma-separated numbers (e.g., "10, 20, 30, 40, 50")

    Returns:
        str: Statistical summary including mean, median, stdev, min, max

    Examples:
        >>> statistics_summary("10, 20, 30, 40, 50")
        "Count: 5
         Mean: 30.0
         Median: 30.0
         Std Dev: 15.81
         Min: 10.0
         Max: 50.0"
    """
    try:
        # Parse numbers from string
        nums = [float(x.strip()) for x in numbers.split(',')]

        if len(nums) < 2:
            return "Error: Need at least 2 numbers for statistics."

        result = f"""Statistical Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Count:      {len(nums)}
Mean:       {statistics.mean(nums):.2f}
Median:     {statistics.median(nums):.2f}
Std Dev:    {statistics.stdev(nums):.2f}
Min:        {min(nums):.2f}
Max:        {max(nums):.2f}
Range:      {max(nums) - min(nums):.2f}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

        return result

    except Exception as e:
        return f"Error: {str(e)}\nPlease provide numbers in format: '10, 20, 30'"


@mcp.tool()
async def currency_convert(amount: float, from_currency: str, to_currency: str, exchange_rate: float) -> str:
    """
    Converts currency using the provided exchange rate.

    Args:
        amount (float): Amount to convert
        from_currency (str): Source currency code (e.g., "USD", "KRW")
        to_currency (str): Target currency code (e.g., "KRW", "USD")
        exchange_rate (float): Exchange rate (how much 1 unit of from_currency equals in to_currency)

    Returns:
        str: Conversion result with formatted output

    Examples:
        >>> currency_convert(1199, "USD", "KRW", 1300)
        "1,199.00 USD = 1,558,700.00 KRW (at rate: 1 USD = 1,300.00 KRW)"
    """
    try:
        result = amount * exchange_rate

        output = f"""Currency Conversion:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Amount:         {amount:,.2f} {from_currency.upper()}
Exchange Rate:  1 {from_currency.upper()} = {exchange_rate:,.4f} {to_currency.upper()}
Result:         {result:,.2f} {to_currency.upper()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

        return output

    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def compare_values(value1: float, value2: float, unit: str = "") -> str:
    """
    Compares two values and shows difference in both absolute and percentage terms.

    Args:
        value1 (float): First value
        value2 (float): Second value
        unit (str): Optional unit label (e.g., "mAh", "GB", "inch")

    Returns:
        str: Comparison result with difference and percentage

    Examples:
        >>> compare_values(4000, 4500, "mAh")
        "Value 1: 4000 mAh
         Value 2: 4500 mAh
         Difference: 500 mAh (12.5% increase)"
    """
    try:
        diff = value2 - value1
        if value1 != 0:
            percent = (diff / value1) * 100
        else:
            percent = 0

        unit_str = f" {unit}" if unit else ""

        direction = "increase" if diff > 0 else "decrease" if diff < 0 else "no change"

        output = f"""Value Comparison:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Value 1:        {value1:,.2f}{unit_str}
Value 2:        {value2:,.2f}{unit_str}
Difference:     {abs(diff):,.2f}{unit_str}
Percentage:     {abs(percent):.2f}% {direction}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

        return output

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
