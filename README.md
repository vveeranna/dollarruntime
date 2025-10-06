# Dollar Checker - RuntimeError with Datadog APM

A Python application that throws an **unhandled RuntimeError** when it detects the `$` character. Fully instrumented with Datadog APM including **Exception Replay**.

## 🎯 What It Does

- Checks text for dollar sign (`$`) character
- **Throws unhandled `RuntimeError`** if `$` is found
- **Script crashes** with full Python stack trace
- **Datadog APM tracks everything** with exception replay
- **Exception Replay captures variable values** at crash time

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Setup Datadog (optional)
cp .env.example .env
# Edit .env with your Datadog API keys

# Run it
python dollar_checker.py "Hello World"    # ✅ Success
python dollar_checker.py "Price: $50"     # 💥 RuntimeError!
```

## ✅ Example: Success (No $)

```bash
$ python dollar_checker.py "Hello World"

======================================================================
Dollar Sign Checker with Datadog APM Exception Replay
======================================================================
✓ Datadog APM initialized
✓ Exception Replay enabled

🔍 Checking text: 'Hello World'
✅ No dollar sign found - text is valid!

======================================================================
✅ SUCCESS - No dollar signs detected!
======================================================================
```

## ❌ Example: Crash (Contains $)

```bash
$ python dollar_checker.py "Price: $50"

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

**Script crashes with unhandled RuntimeError!** 💥

## 🔍 Exception Details

### What You'll See in the Stack Trace

```
RuntimeError: Dollar sign ($) detected at position 7 in text: 'Price: $50'
```

The exception includes:
- **Exception Type**: `RuntimeError`
- **Error Message**: Exact position and text where $ was found
- **Full Stack Trace**: Complete call stack showing where it crashed
- **Line Numbers**: Exact line where exception was raised

### Datadog Exception Replay Captures

- All local variables at crash time
- Function arguments
- Variable values in all stack frames
- Custom debug tags

## 📊 Datadog APM Features

### Metrics
- `dollar_checker.started` - App starts
- `dollar_checker.success` - Successful validations
- `dollar_checker.dollar_found` - Errors (tagged by position)

### Trace Tags
- `input.text` - Input text
- `input.length` - Text length
- `dollar.found` - Boolean
- `dollar.position` - Position of $
- `dollar.context` - Surrounding text
- `error.type` - RuntimeError
- `error.message` - Error details
- `debug.input_text` - Full input
- `debug.character_index` - Exact position
- `debug.before_context` - Text before $
- `debug.after_context` - Text after $

### View in Datadog

1. **APM → Error Tracking**
2. Find **RuntimeError** exceptions
3. Click to view details
4. **Exception Replay tab** - See all variables!

## 🧪 Test Cases

```bash
# Success (no $)
python dollar_checker.py "Hello World"
python dollar_checker.py "50 dollars"
python dollar_checker.py "No special chars"

# Crash (contains $)
python dollar_checker.py "$100"              # RuntimeError at position 0
python dollar_checker.py "Price: $50"        # RuntimeError at position 7
python dollar_checker.py "Pay $25 now"       # RuntimeError at position 4
python dollar_checker.py "Total: $1,000"     # RuntimeError at position 7
```

## 🎨 Why RuntimeError?

`RuntimeError` is a standard Python exception that:
- ✅ Is a built-in exception (no imports needed)
- ✅ Provides clear stack traces
- ✅ Includes custom error messages
- ✅ Is commonly used for runtime errors
- ✅ Works perfectly with Datadog APM
- ✅ Similar to other Python exceptions (like ZeroDivisionError)

## 📁 Files

```
dollar-runtime-error/
├── dollar_checker.py    # Main application
├── requirements.txt     # Dependencies
├── .env.example        # Config template
└── README.md           # This file
```

## 🔧 Configuration

Edit `.env`:
```bash
DD_TRACE_ENABLED=true
DD_API_KEY=your-key
DD_APP_KEY=your-app-key
```

## 💡 Key Features

✅ **RuntimeError Exception** - Standard Python exception  
✅ **Unhandled** - No try/except, crashes immediately  
✅ **Full Stack Trace** - Complete error details  
✅ **Datadog APM** - Complete monitoring  
✅ **Exception Replay** - Variable capture at crash time  
✅ **Custom Error Message** - Shows exact position and text  

---

**Throws RuntimeError on $, fully monitored! 💥📊**
