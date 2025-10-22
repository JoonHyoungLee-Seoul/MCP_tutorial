# Demo Day Checklist ✅
## Pre-Presentation Setup

---

## 📋 1 Day Before

### Environment Setup
- [ ] Test all API keys are working
  - [ ] ANTHROPIC_API_KEY
  - [ ] OPENAI_API_KEY
  - [ ] TAVILY_API_KEY (for web search)
- [ ] Run `pip install -r requirements.txt` to ensure all dependencies
- [ ] Test run the web demo: `streamlit run web_demo.py`
- [ ] Clear output folder: `rm output/*.png output/*.csv`

### Content Preparation
- [ ] Run the iPhone price comparison demo **at least once**
- [ ] Take screenshots of each step
- [ ] Save the final chart as backup
- [ ] Test internet connection speed

### Presentation Files
- [ ] Print or have `DEMO_PRESENTATION.md` open on second screen
- [ ] Have `PRESENTATION_SLIDES.md` converted to slides (optional)
- [ ] Prepare backup screenshots in case of network issues

---

## 🌅 Morning of Presentation

### Technical Check (30 min before)
- [ ] Connect laptop to projector/screen
- [ ] Test display resolution (recommend 1920x1080)
- [ ] Verify internet connection
- [ ] Start Streamlit: `streamlit run web_demo.py`
- [ ] Test the demo query once more
- [ ] Clear browser cache (Cmd+Shift+R on Mac)
- [ ] Close unnecessary apps to free up resources

### Materials Ready
- [ ] Laptop fully charged
- [ ] Backup power adapter plugged in
- [ ] Water bottle nearby
- [ ] Notes/script accessible
- [ ] Backup slides on USB drive (if applicable)

---

## 🎤 5 Minutes Before

### Final Setup
- [ ] Open Streamlit web demo in browser
- [ ] Have the query ready to paste:
  ```
  1. Use Document Retrieval to retrieve iPhone 17 Pro price from documents in euros.
  2. Use tavilysearch to check the currency between euro and Chinese RMB.
  3. Convert the euro price to RMB using the collected information.
  4. Use tavilysearch to check the iPhone 16 Pro price in euros.
  5. Use Code Executor's create_visualization to plot a comparison of the price of iPhone 17 Pro and iPhone 16 Pro.
  6. Show the result
  ```
- [ ] Open GitHub repo in another tab: `https://github.com/JoonHyoungLee-Seoul/MCP_tutorial`
- [ ] Have architecture diagram ready to show
- [ ] Clear output folder one last time

### Mental Preparation
- [ ] Take a deep breath
- [ ] Review key talking points
- [ ] Smile! 😊

---

## 🎬 During Presentation

### Opening (Slide 1-3)
- [ ] Introduce yourself
- [ ] State the demo objective
- [ ] Explain why this is complex

### Live Demo (Slide 18)
- [ ] Switch to Streamlit browser tab
- [ ] Paste the query into text area
- [ ] Click "🚀 Run" button
- [ ] **Point out each step as it executes:**
  - [ ] "Agent is thinking..." (progress bar)
  - [ ] RAG retrieval (document search)
  - [ ] Web search #1 (exchange rate)
  - [ ] Calculator (conversion)
  - [ ] Web search #2 (iPhone 16 Pro price)
  - [ ] Code executor (chart generation)

### Show Results
- [ ] Scroll to "💬 Agent Response" section
- [ ] Read the summary aloud
- [ ] Scroll to "📊 Generated Visualizations"
- [ ] **Make the chart FULL SCREEN** for audience to see
- [ ] Point out price difference

### Highlight Tool Usage
- [ ] Expand "🔧 Tools Used" section
- [ ] Show 4 different tools were used
- [ ] Click one expander to show tool arguments
- [ ] Show the actual result data

### Wrap Up
- [ ] Return to slides
- [ ] Summarize what happened
- [ ] Emphasize: "All from one query!"

---

## ❓ Q&A Preparation

### Expected Questions

**Q: How long does it take?**
- A: "Usually 30-60 seconds for this multi-step query"

**Q: What if a tool fails?**
- A: "The agent tries alternatives or asks for clarification"
- [ ] Can demo: Turn off internet → show error handling

**Q: Can I add my own tools?**
- A: "Yes! Create an MCP server - we have 3 examples in the repo"

**Q: Is the data accurate?**
- A: "RAG uses your trusted documents, web search gets current data, all sources are shown"

**Q: How much does it cost to run?**
- A: "Depends on usage. API costs are minimal - pennies per query for Claude + embeddings"

**Q: Can it work offline?**
- A: "Partially - RAG and calculator yes, web search no"

**Q: What about privacy/security?**
- A: "Your documents stay local, only queries go to LLM APIs"

---

## 🛡️ Backup Plans

### If Internet Fails
- [ ] Have backup screenshots ready
- [ ] Walk through what *would* happen
- [ ] Show the code/architecture instead
- [ ] Explain each step verbally

### If Demo Takes Too Long
- [ ] Explain: "Real-time web search can vary..."
- [ ] Show the progress indicator
- [ ] Talk through what's happening
- [ ] Have backup final screenshot ready

### If Error Occurs
- [ ] Don't panic! Errors happen
- [ ] Read the error message aloud
- [ ] Explain how the system would handle it
- [ ] Use backup screenshots
- [ ] Emphasize: "This is why we have robust error handling"

### If Audience Loses Interest
- [ ] Ask: "What would you use this for?"
- [ ] Take questions mid-demo
- [ ] Show alternative query examples
- [ ] Jump to results if needed

---

## 📊 Alternative Demo Queries

### If Time for Second Demo

**Simpler Query:**
```
Retrieve iPhone 17 Pro battery capacity and iPhone 16 Pro battery capacity from documents, calculate the percentage difference, and create a bar chart.
```

**More Complex:**
```
Search for the top 3 trending smartphones this week, get their prices in USD, convert to EUR using current exchange rate, and create a pie chart showing market share.
```

**Statistical:**
```
Retrieve all iPhone 17 model prices from documents, calculate mean, median, and standard deviation, and create a histogram.
```

---

## 🎯 Key Metrics to Mention

- **12 Tools** available
- **4 Tools** used in this demo
- **6 Steps** executed automatically
- **0 Code** written by user
- **~60 Seconds** execution time
- **95% Time Saved** vs manual process

---

## 📸 Screenshots to Capture (If not done)

### Before Demo
- [ ] Clean interface with query ready
- [ ] Tool categories sidebar
- [ ] Example queries visible

### During Execution
- [ ] Progress bar active
- [ ] Tool selection happening
- [ ] Each tool's status update

### After Completion
- [ ] Full response text
- [ ] Generated chart (FULL SCREEN)
- [ ] Tool usage expanded
- [ ] File browser showing new image

---

## 🎓 Closing Checklist

### After Demo
- [ ] Thank the audience
- [ ] Share GitHub link
- [ ] Offer to stay for questions
- [ ] Share contact info

### Follow-Up
- [ ] Email slides to interested parties
- [ ] Share recording (if recorded)
- [ ] Post demo video on social media
- [ ] Update README with demo video link

---

## 🚨 Emergency Contacts

### Technical Support
- API Status: status.anthropic.com (Claude)
- OpenAI Status: status.openai.com
- Tavily Status: [check their website]

### Backup Presenter
- Name: ___________________
- Phone: ___________________

---

## 💡 Pro Tips

### Voice & Delivery
- Speak slowly and clearly
- Pause after showing results
- Use "we" instead of "I" (inclusive)
- Point to screen when referencing steps

### Audience Engagement
- Make eye contact
- Ask rhetorical questions
- Use hand gestures
- Show enthusiasm!

### Timing
- Start on time
- Leave 5 min buffer for Q&A
- Have a watch/timer visible
- Don't rush if ahead of schedule

### Energy Management
- Deep breaths before starting
- Smile throughout
- Vary your tone
- End on high note

---

## ✅ Post-Presentation

### Immediate (within 1 hour)
- [ ] Save all screenshots
- [ ] Note any issues that occurred
- [ ] Write down questions you couldn't answer
- [ ] Thank organizers

### Within 24 hours
- [ ] Send follow-up email with resources
- [ ] Post about presentation on social media
- [ ] Update documentation if needed
- [ ] Reflect on what went well/what to improve

### Within 1 week
- [ ] Respond to all follow-up questions
- [ ] Share any promised materials
- [ ] Update GitHub with demo video (if recorded)
- [ ] Write blog post about the demo

---

## 🎉 You've Got This!

Remember:
- You know this project inside-out
- The demo is impressive - let it shine
- Mistakes are learning opportunities
- The audience wants you to succeed
- Have fun with it!

**Break a leg! 🚀**
