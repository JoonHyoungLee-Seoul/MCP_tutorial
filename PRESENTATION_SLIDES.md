# Presentation Slides
## LangGraph MCP Multi-Agent System Demo

각 슬라이드는 `---`로 구분되어 있습니다. 이 내용을 Google Slides나 PowerPoint로 옮겨 사용하세요.

---

# Slide 1: Title Slide

## 🤖 LangGraph MCP Multi-Agent System

### Live Demo: Intelligent iPhone Price Comparison

**One Query → Four Tools → Professional Result**

---

# Slide 2: The Challenge

## 🎯 What We Want to Do

**Compare iPhone 17 Pro and iPhone 16 Pro prices in Chinese RMB**

### Why is this complex?

- ❌ Price data in **different sources** (documents vs web)
- ❌ Currency in **different units** (EUR vs RMB)
- ❌ Need **real-time exchange rates**
- ❌ Want **visual comparison chart**

**Normally requires: Multiple tools, manual steps, coding**

---

# Slide 3: Our Solution

## ✅ The Multi-Agent Approach

### One Natural Language Query:

```
1. Retrieve iPhone 17 Pro price from documents (EUR)
2. Search current EUR to RMB exchange rate
3. Convert the price to RMB
4. Search iPhone 16 Pro price (EUR)
5. Create comparison visualization
6. Show the result
```

**Agent figures out the rest! 🚀**

---

# Slide 4: The Workflow

## 🔄 6 Steps, 4 Different Tools

```
User Query
    ↓
📚 RAG: Search Documents → €1,299
    ↓
🔍 Web: Get Exchange Rate → 1 EUR = 7.85 RMB
    ↓
🧮 Calculator: Convert → ¥10,197.15
    ↓
🔍 Web: Get iPhone 16 Pro → €1,199 = ¥9,411.15
    ↓
💻 Code: Generate Chart → 📊 Comparison Graph
    ↓
✅ Result: Text + Visualization
```

---

# Slide 5: Step 1 - Document Retrieval

## 📚 RAG Server in Action

### What happens:
- Searches through PDF documents
- Uses AI-powered semantic search (FAISS)
- Finds relevant information instantly

### Result:
```
iPhone 17 Pro: €1,299
```

**Technology:** Vector similarity search, not keyword matching

---

# Slide 6: Step 2 - Web Search

## 🔍 Real-Time Data Retrieval

### What happens:
- Queries live web for exchange rate
- Validates and extracts data
- Returns structured information

### Result:
```
Exchange Rate: 1 EUR = 7.85 RMB
```

**Technology:** Tavily Search API integration

---

# Slide 7: Step 3 - Calculation

## 🧮 Precise Currency Conversion

### What happens:
- Uses specialized calculator tool
- Applies conversion formula
- Maintains precision

### Calculation:
```
€1,299 × 7.85 = ¥10,197.15
```

**Technology:** MCP Calculator Server

---

# Slide 8: Step 4 - More Data

## 🔍 Second Web Search

### What happens:
- Searches for iPhone 16 Pro pricing
- Extracts and converts currency

### Result:
```
iPhone 16 Pro: €1,199
Converted: ¥9,411.15
```

**Smart: Agent knows to get comparable data**

---

# Slide 9: Step 5 - Visualization

## 💻 Automatic Code Generation

### What happens:
- Agent writes Python code
- Executes safely in isolated environment
- Generates professional chart

### Code (Auto-Generated):
```python
plt.bar(['iPhone 17 Pro', 'iPhone 16 Pro'],
        [10197.15, 9411.15])
plt.title('Price Comparison (RMB)')
plt.savefig('output/comparison.png')
```

**Technology:** Code Executor MCP Server

---

# Slide 10: The Result

## ✅ What the User Sees

### 📊 Visual Chart
![Price Comparison Chart]

### 📝 Summary
```
iPhone 17 Pro: €1,299 (¥10,197)
iPhone 16 Pro: €1,199 (¥9,411)
Difference: ¥786 (7.7% more expensive)
```

**All from ONE natural language query! 🎉**

---

# Slide 11: Behind the Scenes

## 🏗️ System Architecture

### 4 Specialized Agents:

**📚 RAG Server** (1 tool)
- Document search with FAISS

**🧮 Calculator Server** (5 tools)
- Math, statistics, currency conversion

**💻 Code Executor Server** (5 tools)
- Python execution, visualization

**🔍 Web Search** (1 tool)
- Real-time data via Tavily

**Total: 12 Tools** working together!

---

# Slide 12: Technologies Used

## 🔧 Tech Stack

### Core
- **Python** - Programming language
- **LangGraph** - Agent orchestration
- **Claude 3.5 Sonnet** - AI intelligence

### Specialized
- **FastMCP** - Tool protocol
- **FAISS** - Vector search
- **Streamlit** - Web interface

### Libraries
- Pandas, NumPy - Data handling
- Matplotlib - Visualization

---

# Slide 13: Why This Matters

## 💡 Real-World Impact

### ❌ Traditional Approach:
1. Manually search documents → 5 min
2. Google exchange rate → 2 min
3. Open calculator → 1 min
4. Search second product → 3 min
5. Open Excel, create chart → 10 min
**Total: ~20 minutes + manual effort**

### ✅ Our System:
1. Type one query → 5 sec
2. Wait for result → 30-60 sec
**Total: ~1 minute, fully automated**

**Time Saved: 95%** ⚡

---

# Slide 14: Use Cases

## 🎯 Where Can This Help?

### Business
- 📊 Market research automation
- 💰 Financial analysis
- 📈 Competitive intelligence

### Research
- 📚 Literature review
- 🔬 Data analysis
- 📖 Report generation

### Personal
- 🛍️ Shopping comparisons
- 💱 Currency tracking
- 📋 Decision support

---

# Slide 15: What Makes It Special?

## ⭐ Key Differentiators

### 🧠 Intelligent
- Understands natural language
- Plans optimal workflow
- Adapts to errors

### 🔧 Modular
- Add new tools easily
- Each server is independent
- Reusable components

### 🎨 User-Friendly
- No coding required
- Multiple interfaces (Web/CLI/Jupyter)
- Professional results

---

# Slide 16: Extensibility

## 🚀 Easy to Expand

### Current Tools (12):
- RAG, Calculator, Code Executor, Web Search

### Potential New Tools:
- 📧 Email integration
- 🗄️ Database queries
- 🎤 Voice commands
- 🌐 Translation services
- 📷 Image analysis
- ⏰ Scheduling automation

**Add any tool as an MCP server!**

---

# Slide 17: Three Interfaces

## 💻 Choose Your Style

### 🌐 Streamlit Web UI
- Best for: Demos, presentations
- Features: Beautiful GUI, real-time updates

### 💻 Python CLI
- Best for: Quick testing, automation
- Features: Command-line efficiency

### 📓 Jupyter Notebook
- Best for: Learning, development
- Features: Step-by-step exploration

**Same power, different interfaces!**

---

# Slide 18: Live Demo

## 🎬 Let's See It In Action!

### What to watch for:
1. ✅ Natural language input
2. ✅ Automatic tool selection
3. ✅ Real-time progress tracking
4. ✅ Multi-source data integration
5. ✅ Professional output

**[Switch to live demo]**

---

# Slide 19: Results Review

## 📊 What We Just Saw

### Input:
- One complex, multi-step query
- Written in plain English

### Process:
- 4 different tools used
- 6 steps executed automatically
- ~60 seconds total time

### Output:
- Accurate price comparison
- Professional visualization
- Detailed summary

**No coding. No manual steps. Just results.** ✨

---

# Slide 20: Metrics

## 📈 By The Numbers

- **12 Tools** across 4 categories
- **3 User Interfaces** for flexibility
- **4 MCP Servers** working together
- **6 Automated Steps** in this demo
- **0 Lines of Code** from user
- **95% Time Saved** vs manual approach

**Powered by AI, built for humans** 🤖❤️👥

---

# Slide 21: Getting Started

## 🚀 Try It Yourself!

### GitHub Repository:
```
https://github.com/JoonHyoungLee-Seoul/MCP_tutorial
```

### Quick Start:
```bash
git clone [repo-url]
pip install -r requirements.txt
cp .env.example .env
# Add your API keys
streamlit run web_demo.py
```

**Full documentation included!** 📚

---

# Slide 22: Q&A

## ❓ Questions?

### Common Questions:
- How accurate is the data?
- Can it handle errors?
- What's the cost?
- How do I add custom tools?
- Is it production-ready?

**Let's discuss!** 💬

---

# Slide 23: Thank You!

## 🙏 Thank You!

### Resources:
- 📖 **GitHub**: github.com/JoonHyoungLee-Seoul/MCP_tutorial
- 📚 **Documentation**: Full guide in repository
- 🎥 **Video Demo**: [Your link]
- 💬 **Contact**: [Your email]

### Next Steps:
- ⭐ Star the repository
- 🔧 Try it yourself
- 🤝 Contribute & improve

**Questions? Let's connect!** 🚀

---

# Backup Slide: Technical Details

## 🔬 For The Curious

### Architecture:
- **LangGraph**: ReAct agent pattern
- **MCP Protocol**: stdio transport
- **Vector Store**: FAISS with OpenAI embeddings
- **LLM**: Claude 3.5 Sonnet (Anthropic)

### Performance:
- Vector search: <100ms
- Tool execution: 1-5s per tool
- Chart generation: <2s
- Total workflow: 30-90s

---

# Backup Slide: Error Handling

## 🛡️ Robustness

### What if something fails?

**Scenario 1: Document not found**
- Agent tries web search instead

**Scenario 2: Web search timeout**
- Agent uses cached data or asks user

**Scenario 3: Calculation error**
- Agent validates and retries

**Built-in resilience!** ✅

---

# Backup Slide: Comparison

## ⚖️ vs Other Solutions

### Traditional Chatbots
- ❌ No tool use
- ❌ Can't access external data
- ❌ Text-only responses

### Single-Function Tools
- ❌ Limited capabilities
- ❌ Manual workflow
- ❌ No integration

### Our Multi-Agent System
- ✅ 12 specialized tools
- ✅ Automatic orchestration
- ✅ Multimodal output

---

**End of Slides**

---

## 📝 Presenter Notes

### Recommended Timing:
- Slides 1-5: Introduction (3 min)
- Slides 6-10: Step-by-step walkthrough (5 min)
- Slides 11-17: Technical overview (5 min)
- Slide 18: Live demo (3-4 min)
- Slides 19-23: Wrap-up & Q&A (4 min)

**Total: 20-25 minutes**

### Tips:
- Keep backup slides ready for technical questions
- Have live demo tested beforehand
- Prepare screenshots in case of connectivity issues
- Engage audience with questions throughout
