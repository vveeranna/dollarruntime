# Exception Replay Troubleshooting Guide

If you're not seeing Exception Replay in Datadog, follow these steps:

## 🔍 Step 1: Run the Configuration Check

```bash
python check_exception_replay.py
```

This will tell you:
- ✓ If ddtrace is installed and what version
- ✓ If Exception Replay is available
- ✓ If Datadog Agent is running
- ✓ Environment variable status

## 🔧 Step 2: Common Issues and Solutions

### Issue 1: ddtrace Version Too Old

**Symptom:**
```
⚠ Version 1.9.0 may not support Exception Replay
```

**Solution:**
```bash
pip install --upgrade 'ddtrace>=2.0.0'
```

### Issue 2: Exception Replay Not Available

**Symptom:**
```
✗ exception_replay not available
```

**Solution:**
Exception Replay requires:
- ddtrace >= 1.10.0 (preferably >= 2.0.0)
- Python >= 3.7

Update ddtrace:
```bash
pip install --upgrade ddtrace
```

### Issue 3: Datadog Agent Not Running

**Symptom:**
```
✗ Cannot connect to Datadog Agent at localhost:8126
```

**Solution:**

**On macOS:**
```bash
# Check if agent is running
datadog-agent status

# Start agent
datadog-agent start
```

**On Linux:**
```bash
# Check status
sudo systemctl status datadog-agent

# Start agent
sudo systemctl start datadog-agent
```

**Using Docker:**
```bash
docker run -d --name datadog-agent \
  -e DD_API_KEY=<YOUR_API_KEY> \
  -e DD_APM_ENABLED=true \
  -p 8126:8126 \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  gcr.io/datadoghq/agent:latest
```

### Issue 4: API Keys Not Set

**Symptom:**
```
DD_API_KEY: not set
```

**Solution:**
```bash
# Copy example file
cp .env.example .env

# Edit .env and add your keys
nano .env

# Add:
DD_API_KEY=your-actual-api-key-here
DD_APP_KEY=your-actual-app-key-here
```

Get your keys from: https://app.datadoghq.com/organization-settings/api-keys

## 📊 Step 3: Verify Exception Replay in Datadog UI

### Where to Look:

1. **APM → Error Tracking** (Primary location)
   - Service: `dollar-checker`
   - Error Type: `RuntimeError`
   - Click on error
   - Look for tabs: "Exception Replay", "Variables", or "Debug Snapshot"

2. **APM → Traces** (Alternative)
   - Filter: `service:dollar-checker error:true`
   - Click on a trace with error
   - Click on the error span (red)
   - Look for variable information

### What You Should See:

**If Exception Replay is Working:**
- ✓ "Exception Replay" or "Variables" tab visible
- ✓ Local variables shown (text, i, char, etc.)
- ✓ Stack frames with variable values
- ✓ Function arguments displayed

**If Not Working:**
- ✗ Only "Stack Trace" tab
- ✗ No variable values
- ✗ No "Exception Replay" tab

## 🎯 Step 4: Alternative - Use Error Tracking Without Exception Replay

If Exception Replay isn't available, you can still see rich error information through our custom tags:

### Custom Tags We Added:

```python
# These are ALWAYS sent, even without Exception Replay
debug.input_text: "Price: $50"
debug.character_index: 7
debug.before_context: "Price: "
debug.after_context: "50"
dollar.position: 7
dollar.context: "rice: $50"
error.type: "RuntimeError"
error.message: "Dollar sign found at position 7"
```

### Where to Find Custom Tags:

1. Go to: **APM → Error Tracking**
2. Click on **RuntimeError**
3. Click on **"Span Details"** or **"Tags"** tab
4. Look for tags starting with `debug.*`, `dollar.*`, `error.*`

These tags give you similar debugging information even without Exception Replay!

## 🔬 Step 5: Test Exception Replay

### Test Script:

```bash
# 1. Upgrade ddtrace
pip install --upgrade 'ddtrace>=2.0.0'

# 2. Check configuration
python check_exception_replay.py

# 3. Run the app
python dollar_checker.py "Price: $50"

# 4. Check output for:
✓ Exception Replay enabled

# 5. Wait 30 seconds for data to reach Datadog

# 6. Go to Datadog:
# https://app.datadoghq.com/apm/error-tracking
```

## 📋 Checklist

Before reporting that Exception Replay isn't working, verify:

- [ ] ddtrace >= 2.0.0 installed (`pip list | grep ddtrace`)
- [ ] Python >= 3.7 (`python --version`)
- [ ] Datadog Agent running (`curl http://localhost:8126/info`)
- [ ] DD_API_KEY set in .env
- [ ] DD_TRACE_ENABLED=true in .env
- [ ] App shows "✓ Exception Replay enabled" when running
- [ ] Exception was actually thrown (RuntimeError)
- [ ] Waited at least 30 seconds for data to reach Datadog
- [ ] Looking in correct place (APM → Error Tracking)
- [ ] Correct service name (`dollar-checker`)

## 🆘 Still Not Working?

### Option 1: Check ddtrace Documentation

Exception Replay feature details:
https://docs.datadoghq.com/tracing/error_tracking/exception_replay/

### Option 2: Use Custom Tags Instead

Our app already sends rich debugging information via custom tags (see Step 4 above). These work regardless of Exception Replay availability.

### Option 3: Enable Debug Logging

Add to your .env:
```bash
DD_TRACE_DEBUG=true
DD_TRACE_STARTUP_LOGS=true
```

Run the app and check output for any errors.

### Option 4: Verify Feature Availability

Exception Replay may not be available in all Datadog plans or regions. Check:
- Your Datadog plan includes APM
- Your region supports Exception Replay
- Feature is enabled in your organization settings

## 💡 Alternative: Manual Variable Logging

If Exception Replay doesn't work, you can manually log variables:

```python
# Add before raising exception
import logging
logging.error(f"Exception about to be raised: text={text}, i={i}, char={char}")
raise RuntimeError(...)
```

## 📞 Support

- Datadog Support: https://www.datadoghq.com/support/
- Datadog Community: https://datadoghq.slack.com/
- GitHub Issues: https://github.com/DataDog/dd-trace-py/issues

---

**Remember: Even without Exception Replay, our custom tags provide excellent debugging information!** 🎯
