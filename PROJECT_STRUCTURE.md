# Project Structure

This document provides a detailed overview of the project's directory structure and file organization.

## Directory Tree

```
lee_mcp_tutorial/
├── 📓 User Interfaces (3 interfaces)
│   ├── agent.py                   # Python CLI interface
│   ├── web_demo.py                # Streamlit web interface
│   └── utils_streamlit.py         # Streamlit utility functions
│
├── 🤖 MCP Servers (3 servers, 11 tools)
│   ├── mcp_server_rag.py          # RAG retriever (1 tool)
│   ├── mcp_server_calculator.py   # Calculator (5 tools)
│   └── mcp_server_code_executor.py# Code executor (5 tools)
│
├── 🔧 Utilities
│   ├── utils.py                   # Core streaming utilities
│   └── .env                       # Environment variables
│
├── 📁 Data & Output
│   ├── data/                      # PDF documents for RAG
│   │   ├── *.pdf                  # Place PDF files here
│   │   └── *.faiss                # FAISS index (auto-generated)
│   └── output/                    # Generated files
│       ├── *.png                  # Visualizations
│       ├── *.csv                  # Data exports
│       └── .gitkeep               # Preserve directory
│
├── 📚 Examples
│   └── MCP.ipynb                  # Jupyter notebook tutorial
│
├── 🧪 Tests
│   ├── test_agent_init.py         # Test agent initialization
│   ├── test_calculator.py         # Test calculator tools
│   └── test_visualization.py      # Test visualization generation
│
├── 📖 Documentation (in docs/)
│   ├── QUICK_START.md             # Quick start guide
│   ├── USAGE_GUIDE.md             # Detailed usage
│   ├── CALCULATOR_USAGE.md        # Calculator tools guide
│   ├── CODE_EXECUTOR_USAGE.md     # Code executor guide
│   ├── NOTEBOOK_EXAMPLES.md       # Example queries
│   ├── FIX_NOTES.md               # Event loop fix notes
│   ├── VISUALIZATION_FIX.md       # Visualization display fix
│   ├── WEB_DEMO_IMPROVEMENTS.md   # Web demo features
│   ├── EMPTY_CHART_FIX.md         # Chart debugging guide
│   └── STREAMLIT_UI_PREVIEW.md    # UI preview screenshots
│
└── 📋 Configuration
    ├── requirements.txt           # Python dependencies
    ├── .gitignore                 # Git ignore rules
    ├── README.md                  # Main README (English)
    ├── README_KOR.md              # Korean README
    ├── RUN_WEB_DEMO.sh            # Web demo launcher
    └── PROJECT_STRUCTURE.md       # This file
```

## File Categories

### User Interfaces

These files provide different ways to interact with the MCP agent system.

#### `agent.py`
**Type**: Python CLI
**Purpose**: Standalone command-line interface
**Best for**: Quick testing, automation, script integration

**Features**:
- Interactive REPL loop
- Exports `create_mcp_agent()` function
- Event loop handling for multiple environments
- Works in Jupyter, CLI, and Streamlit

**Usage**:
```bash
python agent.py
```

#### `web_demo.py`
**Type**: Streamlit Web App
**Purpose**: Web-based GUI for agent interaction
**Best for**: Demos, presentations, non-technical users

**Features**:
- Beautiful UI with example queries
- Real-time agent execution monitoring
- Auto-display of generated visualizations
- Tool usage tracking
- File browser for outputs

**Usage**:
```bash
streamlit run web_demo.py
```

#### `utils_streamlit.py`
**Type**: Utility Module
**Purpose**: Streamlit-specific helper functions

**Functions**:
- `display_agent_response_streamlit()`: Renders agent responses with UI
- `astream_graph_streamlit()`: Graph streaming for Streamlit
- `get_tool_icon()`: Maps tool names to emoji icons
- `format_tool_result()`: Formats tool results for display

### MCP Servers

These files implement MCP (Model Context Protocol) servers that provide tools to the agent.

#### `mcp_server_rag.py`
**Tools**: 1 (`retrieve`)
**Purpose**: Document retrieval via RAG

**Features**:
- FAISS vector store
- PDF document processing
- Text chunking with RecursiveCharacterTextSplitter
- OpenAI embeddings (text-embedding-3-small)
- Global caching for performance

**Tool**:
```python
retrieve(query: str) -> str
# Search documents and return relevant information
```

#### `mcp_server_calculator.py`
**Tools**: 5 tools
**Purpose**: Mathematical calculations and statistics

**Tools**:
```python
calculate(expression: str) -> float
# Evaluate math expressions (supports trig, log, sqrt, etc.)

percentage_change(old_value: float, new_value: float) -> float
# Calculate percentage change

statistics_summary(numbers: List[float]) -> dict
# Calculate mean, median, std, min, max

currency_convert(amount: float, rate: float, from_currency: str, to_currency: str) -> str
# Convert currency

compare_values(values: dict) -> str
# Compare and analyze values
```

#### `mcp_server_code_executor.py`
**Tools**: 5 tools
**Purpose**: Python code execution and data visualization

**Tools**:
```python
execute_python(code: str) -> str
# Execute Python code safely (pandas, numpy, matplotlib)

create_visualization(data: str, chart_type: str, title: str, ...) -> str
# Create charts (line, bar, scatter, pie, hist)

analyze_data(data: str, analysis_type: str) -> str
# Data analysis (statistics, grouping, correlation)

read_csv(filepath: str) -> str
# Read CSV files

save_to_csv(data: str, filepath: str) -> str
# Save data to CSV
```

### Utilities

#### `utils.py`
**Type**: Core Utilities
**Purpose**: Agent execution and streaming

**Functions**:
```python
async def astream_graph(graph, inputs, config)
# Stream agent execution with real-time updates

def print_tool_info(node_name, chunk_data)
# Display tool usage with color coding
```

**Features**:
- Real-time streaming output
- Color-coded messages (🔧 Tool Selected, ✅ Tool Executed)
- Tool argument and result tracking

### Data & Output

#### `data/`
**Purpose**: Store PDF documents for RAG retrieval

**Contents**:
- PDF files (manually added)
- FAISS index files (auto-generated)
- Pickle files (auto-generated)

**Note**: FAISS indices are gitignored and regenerated on first use.

#### `output/`
**Purpose**: Store generated files (charts, CSVs)

**Contents**:
- PNG images (charts)
- CSV files (data exports)

**Note**: Output files are gitignored (except .gitkeep) to avoid repository bloat.

### Examples

#### `examples/MCP.ipynb`
**Type**: Jupyter Notebook
**Purpose**: Interactive tutorial and examples

**Contents**:
- Environment setup
- MCP server initialization
- Agent creation
- Example queries
- Step-by-step walkthroughs

### Tests

#### `tests/test_agent_init.py`
Tests agent initialization and tool loading.

#### `tests/test_calculator.py`
Tests calculator MCP tools (calculate, percentage_change, etc.).

#### `tests/test_visualization.py`
Tests visualization creation with debug output.

### Documentation

See `docs/` folder for comprehensive guides:

- **QUICK_START.md**: Fast setup and 3 usage methods
- **USAGE_GUIDE.md**: Detailed instructions for all features
- **CALCULATOR_USAGE.md**: Calculator MCP server documentation
- **CODE_EXECUTOR_USAGE.md**: Code executor documentation
- **NOTEBOOK_EXAMPLES.md**: Collection of example queries
- **FIX_NOTES.md**: Event loop fixes for Streamlit
- **VISUALIZATION_FIX.md**: Visualization display fixes
- **WEB_DEMO_IMPROVEMENTS.md**: Web demo features
- **EMPTY_CHART_FIX.md**: Debugging empty charts
- **STREAMLIT_UI_PREVIEW.md**: UI screenshots

### Configuration

#### `requirements.txt`
Python package dependencies:
- anthropic, langchain, langgraph
- mcp, fastmcp
- faiss-cpu, sentence-transformers
- streamlit, matplotlib, pandas
- etc.

#### `.gitignore`
Ignores:
- Python cache (`__pycache__`)
- Environment variables (`.env`)
- Generated outputs (`output/*.png`)
- OS metadata (`.DS_Store`)
- Virtual environments (`venv/`)

#### `RUN_WEB_DEMO.sh`
Convenience script to launch Streamlit web demo.

## Ignored Files (Not in Git)

The following are automatically generated or contain sensitive data:

```
__pycache__/          # Python bytecode cache
*.pyc                 # Compiled Python files
.env                  # API keys and secrets
.DS_Store             # macOS metadata
output/*.png          # Generated visualizations
output/*.csv          # Generated data files
data/*.faiss          # FAISS vector indices
data/*.pkl            # Pickle files
venv/                 # Virtual environment
```

## Quick Reference

### To Run the Project

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file with API keys
# (See README.md for required keys)

# 3. Add PDF documents to data/

# 4. Choose an interface:
python agent.py              # CLI
streamlit run web_demo.py    # Web UI
jupyter notebook examples/MCP.ipynb  # Notebook
```

### To Add New MCP Tools

1. Create `mcp_server_*.py` file
2. Use `@mcp.tool()` decorator
3. Update `agent.py` to load the new server
4. Update documentation

### To Add New Tests

1. Create `tests/test_*.py` file
2. Import agent and tools
3. Write test cases
4. Run with `python tests/test_*.py`

## Architecture Overview

```
User Query
    ↓
Agent (agent.py)
    ↓
LangGraph ReAct Loop
    ↓
Tool Selection
    ↓
┌─────────────┬──────────────┬────────────────┬─────────────┐
│ RAG Server  │ Calculator   │ Code Executor  │ TavilySearch│
│ (1 tool)    │ (5 tools)    │ (5 tools)      │ (1 tool)    │
└─────────────┴──────────────┴────────────────┴─────────────┘
    ↓
Tool Execution Results
    ↓
Agent Reasoning
    ↓
Final Response (Text + Generated Files)
```

## Notes

- **Total Tools**: 12 (1 RAG + 5 Calculator + 5 Code Executor + 1 Web Search)
- **Interfaces**: 3 (Jupyter, CLI, Web)
- **MCP Servers**: 3 (RAG, Calculator, Code Executor)
- **Documentation Files**: 10+ guides in `docs/`

---

For more information, see [README.md](./README.md) and [docs/QUICK_START.md](./docs/QUICK_START.md).
