# Fixed: TypeError with hostname parameter

## Error You Encountered

```
TypeError: configure() got an unexpected keyword argument 'hostname'
```

## What Happened

In newer versions of ddtrace (2.x), the `tracer.configure()` method no longer accepts `hostname` and `port` parameters. Instead, you should use environment variables.

## Fix Applied

### Old Code (Caused Error):
```python
tracer.configure(
    hostname=os.environ.get('DD_AGENT_HOST', 'localhost'),
    port=int(os.environ.get('DD_AGENT_PORT', 8126)),
)
```

### New Code (Fixed):
```python
# Use environment variables instead
agent_url = f"http://{os.environ.get('DD_AGENT_HOST', 'localhost')}:{os.environ.get('DD_TRACE_AGENT_PORT', '8126')}"
os.environ.setdefault('DD_TRACE_AGENT_URL', agent_url)
```

## How to Use

### Option 1: Using Environment Variables (Recommended)

Set in your `.env` file or environment:
```bash
DD_AGENT_HOST=localhost
DD_TRACE_AGENT_PORT=8126
```

### Option 2: Using Full Agent URL

Set in your `.env` file:
```bash
DD_TRACE_AGENT_URL=http://localhost:8126
```

### Option 3: For Remote Agent

If your Datadog Agent is on a different host:
```bash
DD_AGENT_HOST=datadog-agent.example.com
DD_TRACE_AGENT_PORT=8126
```

Or:
```bash
DD_TRACE_AGENT_URL=http://datadog-agent.example.com:8126
```

## Now You Can Run

```bash
python dollar_checker.py "Price: $50"
```

Expected output:
```
✓ Exception Replay enabled
✓ Datadog APM initialized

🔍 Checking text: 'Price: $50'

❌ DOLLAR SIGN DETECTED at position 7!
   Character: '$'
   Position: 7
   Context: ...rice: $50...

💥 Throwing unhandled RuntimeError exception...

Traceback (most recent call last):
  ...
RuntimeError: Dollar sign ($) detected at position 7 in text: 'Price: $50'
```

## Verify It Works

1. Run the app:
   ```bash
   python dollar_checker.py "test $"
   ```

2. Should see:
   - ✓ Exception Replay enabled
   - ✓ Datadog APM initialized
   - RuntimeError thrown

3. Check Datadog:
   - Go to APM → Error Tracking
   - Find RuntimeError
   - See exception details

---

**Error fixed! The app should now run without the TypeError.** ✅
