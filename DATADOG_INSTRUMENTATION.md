# Datadog APM Instrumentation Guide

This document explains all the Datadog APM instrumentation in the dollar checker application.

## ✅ Instrumentation Components

### 1. **Datadog APM Libraries** (Lines 14-16)

```python
from ddtrace import tracer, patch_all, config
import datadog
```

- `ddtrace` - Datadog tracing library
- `tracer` - For creating custom spans
- `patch_all()` - Auto-instruments all supported libraries
- `config` - For configuring APM features
- `datadog` - For custom metrics (StatsD)

### 2. **Exception Replay Enabled** (Line 19)

```python
config.exception_replay.enabled = True
```

**What it does:**
- Captures variable values when exceptions occur
- Records local variables in all stack frames
- Stores function arguments at crash time
- Available in Datadog Error Tracking UI

### 3. **Auto-Instrumentation** (Line 22)

```python
patch_all()
```

**What it patches:**
- HTTP libraries (requests, urllib, etc.)
- Database drivers (psycopg2, mysql, etc.)
- Web frameworks (Flask, Django, etc.)
- Redis, MongoDB, and other integrations

### 4. **Tracer Configuration** (Lines 28-31)

```python
tracer.configure(
    hostname=os.environ.get('DD_AGENT_HOST', 'localhost'),
    port=int(os.environ.get('DD_AGENT_PORT', 8126)),
)
```

**Configures:**
- Agent hostname (where to send traces)
- Agent port (default: 8126)
- Connection to Datadog Agent

### 5. **Datadog API Initialization** (Lines 33-36)

```python
datadog.initialize(
    api_key=os.environ.get('DD_API_KEY'),
    app_key=os.environ.get('DD_APP_KEY'),
)
```

**Enables:**
- Custom metrics via StatsD
- Direct API access
- Metric submission

## 📊 Custom Instrumentation

### 6. **Function Tracing with @tracer.wrap** (Lines 41, 114)

```python
@tracer.wrap(service='dollar-checker', resource='check_for_dollar')
def check_for_dollar(text):
    ...

@tracer.wrap(service='dollar-checker', resource='main')
def main():
    ...
```

**Creates:**
- Automatic span for each function call
- Service name: `dollar-checker`
- Resource names: `check_for_dollar`, `main`
- Timing information
- Automatic error tracking

### 7. **Custom Span Tags** (Lines 56-61, 86-97, 141-144)

```python
span = tracer.current_span()
if span:
    span.set_tag('app.name', 'dollar-checker')
    span.set_tag('input.text', text)
    span.set_tag('input.length', len(text))
    span.set_tag('check.character', '$')
```

**Tags Added:**
- `app.name` - Application name
- `app.version` - Version number
- `app.environment` - Environment (dev/prod)
- `input.text` - Input text
- `input.length` - Text length
- `check.character` - Character being checked

### 8. **Error Tags** (Lines 86-97)

```python
span.set_tag('error', True)
span.set_tag('error.type', 'RuntimeError')
span.set_tag('error.message', f'Dollar sign found at position {i}')
span.set_tag('dollar.found', True)
span.set_tag('dollar.position', i)
span.set_tag('dollar.context', text[max(0,i-5):i+6])
```

**Error Information:**
- `error` - Boolean flag
- `error.type` - Exception type
- `error.message` - Error description
- `dollar.found` - Whether $ was found
- `dollar.position` - Exact position
- `dollar.context` - Surrounding text

### 9. **Debug Tags for Exception Replay** (Lines 93-97)

```python
span.set_tag('debug.input_text', text)
span.set_tag('debug.character_index', i)
span.set_tag('debug.before_context', text[:i])
span.set_tag('debug.after_context', text[i+1:])
```

**Debug Information:**
- Full input text
- Character index
- Text before error
- Text after error

### 10. **Custom Metrics (StatsD)** (Lines 75-81, 107-111, 128, 136)

```python
datadog.statsd.increment('dollar_checker.dollar_found', tags=[...])
datadog.statsd.increment('dollar_checker.success')
datadog.statsd.increment('dollar_checker.started')
datadog.statsd.increment('dollar_checker.no_input')
```

**Metrics Tracked:**
- `dollar_checker.started` - App starts
- `dollar_checker.success` - Successful validations
- `dollar_checker.dollar_found` - Errors (with position tags)
- `dollar_checker.no_input` - Missing input errors

**Metric Tags:**
- `position:{i}` - Position of $
- `status:error` - Error status
- `exception:RuntimeError` - Exception type

## 🔍 What Gets Tracked in Datadog

### APM Traces
1. **Service**: `dollar-checker`
2. **Resources**: 
   - `check_for_dollar` - Main validation function
   - `main` - Entry point
3. **Spans**: Automatic timing for each function
4. **Tags**: All custom tags listed above

### Error Tracking
1. **Exception Type**: RuntimeError
2. **Error Message**: Full error with position and text
3. **Stack Trace**: Complete Python traceback
4. **Exception Replay**: Variable values at crash time
5. **Custom Tags**: All debug and error tags

### Custom Metrics
1. **Counters**:
   - Application starts
   - Successful validations
   - Errors (by position)
   - Missing input errors

2. **Tags on Metrics**:
   - Position of error
   - Status (error/success)
   - Exception type

## 📈 Viewing in Datadog

### 1. APM Traces
```
Navigate to: APM → Traces
Filter by: service:dollar-checker
```

You'll see:
- All function calls
- Timing information
- Custom tags
- Error flags

### 2. Error Tracking
```
Navigate to: APM → Error Tracking
Filter by: service:dollar-checker
```

You'll see:
- RuntimeError exceptions
- Stack traces
- Exception Replay data
- Variable values at crash

### 3. Custom Metrics
```
Navigate to: Metrics → Explorer
Search for: dollar_checker.*
```

Available metrics:
- `dollar_checker.started`
- `dollar_checker.success`
- `dollar_checker.dollar_found`
- `dollar_checker.no_input`

### 4. Service Map
```
Navigate to: APM → Service Map
```

Shows:
- `dollar-checker` service
- Dependencies
- Error rates
- Throughput

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Enable/disable tracing
DD_TRACE_ENABLED=true

# Datadog API credentials
DD_API_KEY=your-datadog-api-key
DD_APP_KEY=your-datadog-app-key

# Agent connection
DD_AGENT_HOST=localhost
DD_AGENT_PORT=8126

# Service metadata
DD_SERVICE=dollar-checker
DD_ENV=development
DD_VERSION=1.0.0
```

### Service Tags

The application automatically tags traces with:
- `service:dollar-checker`
- `env:development` (from DD_ENV)
- `version:1.0.0` (from DD_VERSION)

## 🎯 Exception Replay Details

When RuntimeError is thrown, Exception Replay captures:

### Local Variables
```python
text = "Price: $50"
i = 7
char = '$'
span = <Span object>
```

### Function Arguments
```python
check_for_dollar(text='Price: $50')
```

### Stack Frames
- All local variables in each frame
- Function names and line numbers
- Variable values at crash time

### Custom Debug Data
- `debug.input_text`: Full input
- `debug.character_index`: 7
- `debug.before_context`: "Price: "
- `debug.after_context`: "50"

## ✅ Verification Checklist

- [x] Datadog APM library imported
- [x] Exception Replay enabled
- [x] Auto-instrumentation (patch_all)
- [x] Tracer configured
- [x] Datadog API initialized
- [x] Functions wrapped with @tracer.wrap
- [x] Custom span tags added
- [x] Error tags added
- [x] Debug tags for exception replay
- [x] Custom metrics (StatsD)
- [x] Metric tags configured
- [x] Environment variables documented
- [x] Service name set
- [x] Resource names set

## 🚀 Running with Datadog

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup environment
cp .env.example .env
# Edit .env with your Datadog keys

# 3. Ensure Datadog Agent is running
# Check: http://localhost:8126/info

# 4. Run the app
python dollar_checker.py "test $"

# 5. View in Datadog
# APM → Traces → service:dollar-checker
# APM → Error Tracking → RuntimeError
```

## 📊 Expected Datadog Data

### On Success
- ✅ Trace with 2 spans (main, check_for_dollar)
- ✅ Metric: `dollar_checker.started` +1
- ✅ Metric: `dollar_checker.success` +1
- ✅ Tags: `validation.passed:true`, `dollar.found:false`

### On Error ($ found)
- ❌ Trace with error flag
- ❌ RuntimeError in Error Tracking
- ❌ Exception Replay data available
- ❌ Metric: `dollar_checker.dollar_found` +1
- ❌ Tags: `error:true`, `dollar.found:true`, `dollar.position:X`

---

**Fully instrumented with Datadog APM! 📊✅**
