# Datadog Exception Replay - Complete Guide

This guide shows you how to see and use Datadog's Exception Replay feature with this application.

## 🎯 What is Exception Replay?

Exception Replay captures the **complete state of your application** when an exception occurs, including:
- ✅ All local variable values
- ✅ Function arguments
- ✅ Variable values in every stack frame
- ✅ The exact state that caused the crash

**It's like time-travel debugging!** You can see exactly what your variables contained when the exception was thrown.

## ✅ Exception Replay is Already Enabled

### Line 19 in `dollar_checker.py`:

```python
# Enable exception replay and profiling
config.exception_replay.enabled = True
```

This single line enables the entire Exception Replay feature!

## 🚀 How to See Exception Replay in Action

### Step 1: Setup and Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure Datadog
cp .env.example .env
# Edit .env and add your DD_API_KEY and DD_APP_KEY

# 3. Make sure Datadog Agent is running
# Check: http://localhost:8126/info

# 4. Run the app with a $ character to trigger exception
python dollar_checker.py "Price: $50"
```

### Step 2: Expected Output

```
======================================================================
Dollar Sign Checker with Datadog APM Exception Replay
======================================================================
✓ Datadog APM initialized
✓ Exception Replay enabled

🔍 Checking text: 'Price: $50'

❌ DOLLAR SIGN DETECTED at position 7!
   Character: '$'
   Position: 7
   Context: ...rice: $50...

💥 Throwing unhandled RuntimeError exception...

Traceback (most recent call last):
  File "dollar_checker.py", line 154, in <module>
    exit_code = main()
  File "dollar_checker.py", line 149, in main
    check_for_dollar(text)
  File "dollar_checker.py", line 100, in check_for_dollar
    raise RuntimeError(f"Dollar sign ($) detected at position {i} in text: '{text}'")
RuntimeError: Dollar sign ($) detected at position 7 in text: 'Price: $50'
```

### Step 3: View in Datadog

#### Option A: Via APM Error Tracking

1. **Go to Datadog**: https://app.datadoghq.com
2. **Navigate to**: APM → Error Tracking
3. **Filter by service**: `dollar-checker`
4. **Find the error**: Look for `RuntimeError`
5. **Click on the error** to open details

#### Option B: Via APM Traces

1. **Go to**: APM → Traces
2. **Filter**: `service:dollar-checker` AND `error:true`
3. **Click on a trace** with an error
4. **Look for the error span** (highlighted in red)
5. **Click on the span** to see details

## 🔍 What You'll See in Exception Replay

### 1. **Error Overview**

```
RuntimeError: Dollar sign ($) detected at position 7 in text: 'Price: $50'
```

### 2. **Stack Trace**

```
Traceback (most recent call last):
  File "dollar_checker.py", line 154, in <module>
    exit_code = main()
  File "dollar_checker.py", line 149, in main
    check_for_dollar(text)
  File "dollar_checker.py", line 100, in check_for_dollar
    raise RuntimeError(...)
```

### 3. **Exception Replay Tab** (The Magic Part!)

Click on the **"Exception Replay"** or **"Variables"** tab to see:

#### Frame 1: `check_for_dollar` (where exception was raised)

**Local Variables:**
```python
text = "Price: $50"
i = 7
char = '$'
span = <Span object at 0x...>
DD_TRACE_ENABLED = True
```

**Function Arguments:**
```python
text = "Price: $50"
```

#### Frame 2: `main` (calling function)

**Local Variables:**
```python
text = "Price: $50"
span = <Span object at 0x...>
DD_TRACE_ENABLED = True
```

#### Frame 3: `<module>` (top level)

**Local Variables:**
```python
exit_code = (not yet assigned)
```

### 4. **Custom Tags** (Also visible)

In the trace details, you'll see all the custom tags we added:

```
debug.input_text: "Price: $50"
debug.character_index: 7
debug.before_context: "Price: "
debug.after_context: "50"
dollar.found: true
dollar.position: 7
dollar.context: "rice: $50"
error: true
error.type: "RuntimeError"
error.message: "Dollar sign found at position 7"
input.text: "Price: $50"
input.length: 10
check.character: "$"
```

## 📸 Screenshot Guide

### Where to Find Exception Replay in Datadog UI

1. **APM → Error Tracking**
   ```
   [Service: dollar-checker] [Error Type: RuntimeError]
   ```

2. **Click on the error issue**
   ```
   Shows: Error count, first seen, last seen
   ```

3. **Click on a specific occurrence**
   ```
   Shows: Full error details
   ```

4. **Look for tabs:**
   - **Overview** - Error message and count
   - **Stack Trace** - Full Python traceback
   - **Exception Replay** / **Variables** - 🎯 THIS IS IT!
   - **Span Details** - APM trace information

5. **In the Exception Replay/Variables tab:**
   ```
   You'll see a tree view of:
   ├── Frame: check_for_dollar (line 100)
   │   ├── text: "Price: $50"
   │   ├── i: 7
   │   ├── char: "$"
   │   └── span: <Span>
   ├── Frame: main (line 149)
   │   └── text: "Price: $50"
   └── Frame: <module> (line 154)
   ```

## 🧪 Test Different Scenarios

### Test 1: $ at the beginning
```bash
python dollar_checker.py "$100"
```

**Exception Replay will show:**
```python
i = 0
char = '$'
text = "$100"
```

### Test 2: $ in the middle
```bash
python dollar_checker.py "Pay $25 now"
```

**Exception Replay will show:**
```python
i = 4
char = '$'
text = "Pay $25 now"
```

### Test 3: $ at the end
```bash
python dollar_checker.py "Total: $"
```

**Exception Replay will show:**
```python
i = 7
char = '$'
text = "Total: $"
```

## 🔧 Troubleshooting

### "I don't see the Exception Replay tab"

**Possible reasons:**

1. **Exception Replay not enabled**
   - Check line 19: `config.exception_replay.enabled = True` ✅ Already enabled!

2. **ddtrace version too old**
   ```bash
   pip install --upgrade ddtrace
   # Requires ddtrace >= 1.10.0
   ```

3. **Datadog Agent not running**
   ```bash
   # Check agent status
   curl http://localhost:8126/info
   ```

4. **Environment variable disabled**
   ```bash
   # Make sure in .env:
   DD_TRACE_ENABLED=true
   ```

### "Variables show as <unavailable>"

This can happen if:
- Variables were optimized away by Python
- Variables went out of scope
- Privacy settings in Datadog

**Solution:** Our code has many variables at the exception point, so you should see them all!

## 💡 Why Exception Replay is Powerful

### Traditional Debugging:
```
❌ Exception occurs in production
❌ Try to reproduce locally
❌ Add more logging
❌ Deploy again
❌ Wait for it to happen again
❌ Still don't know the exact values
```

### With Exception Replay:
```
✅ Exception occurs
✅ Open Datadog
✅ See exact variable values
✅ Understand the problem immediately
✅ Fix it
✅ Done!
```

## 📊 What Gets Captured

### Automatically Captured:
- ✅ All local variables
- ✅ Function arguments
- ✅ Variables in all stack frames
- ✅ Variable types and values
- ✅ Object attributes (for objects)

### Custom Tags We Added:
- ✅ `debug.input_text` - Full input
- ✅ `debug.character_index` - Exact position
- ✅ `debug.before_context` - Text before $
- ✅ `debug.after_context` - Text after $
- ✅ `dollar.position` - Position of $
- ✅ `dollar.context` - Surrounding text

## 🎯 Real-World Example

**Scenario:** User reports "app crashes with certain input"

**Without Exception Replay:**
- Ask user for exact input
- Try to reproduce
- Add logging
- Deploy
- Wait...

**With Exception Replay:**
1. Open Datadog Error Tracking
2. See the exact input: `text = "Price: $50"`
3. See the exact position: `i = 7`
4. See the character: `char = '$'`
5. **Immediately understand**: App crashes when $ is in the input
6. Fix it!

## 🚀 Quick Start Checklist

- [x] Exception Replay enabled (line 19)
- [x] ddtrace installed
- [x] Datadog Agent running
- [x] Environment variables set
- [ ] Run app with $ character
- [ ] Check Datadog Error Tracking
- [ ] Click on RuntimeError
- [ ] View Exception Replay tab
- [ ] See all variable values!

## 📝 Code Reference

### Where Exception Replay is Enabled:
```python
# Line 19 in dollar_checker.py
config.exception_replay.enabled = True
```

### Where Exception is Thrown:
```python
# Line 100 in dollar_checker.py
raise RuntimeError(f"Dollar sign ($) detected at position {i} in text: '{text}'")
```

### Variables Available at Exception Time:
```python
text = "Price: $50"    # The full input text
i = 7                  # Position where $ was found
char = '$'             # The character that caused the error
span = <Span>          # Datadog span object
```

## 🎓 Learn More

- [Datadog Exception Replay Docs](https://docs.datadoghq.com/tracing/error_tracking/exception_replay/)
- [Error Tracking Guide](https://docs.datadoghq.com/tracing/error_tracking/)
- [APM Python Setup](https://docs.datadoghq.com/tracing/setup_overview/setup/python/)

---

**Exception Replay is enabled and ready to use! Run the app and check Datadog! 🎯📊**
