#!/usr/bin/env python3
"""
Check if Exception Replay is properly configured
"""

import sys

print("=" * 70)
print("Datadog Exception Replay Configuration Check")
print("=" * 70)
print()

# Check Python version
print(f"✓ Python version: {sys.version}")
print()

# Check ddtrace installation
try:
    import ddtrace
    print(f"✓ ddtrace installed: version {ddtrace.__version__}")
    
    # Check if version supports exception replay
    version_parts = ddtrace.__version__.split('.')
    major = int(version_parts[0])
    minor = int(version_parts[1]) if len(version_parts) > 1 else 0
    
    if major >= 2 or (major == 1 and minor >= 10):
        print("  ✓ Version supports Exception Replay (>= 1.10.0)")
    else:
        print(f"  ⚠ Version {ddtrace.__version__} may not support Exception Replay")
        print("  → Upgrade with: pip install --upgrade 'ddtrace>=2.0.0'")
except ImportError:
    print("✗ ddtrace not installed")
    print("  → Install with: pip install ddtrace")
    sys.exit(1)

print()

# Check exception replay feature
try:
    from ddtrace import config
    print("✓ ddtrace.config available")
    
    # Try to enable exception replay
    try:
        config.exception_replay.enabled = True
        print("  ✓ config.exception_replay.enabled = True")
        print(f"  ✓ Current value: {config.exception_replay.enabled}")
    except AttributeError as e:
        print(f"  ✗ exception_replay not available: {e}")
        print("  → This feature may not be available in your ddtrace version")
    
    # Try dynamic instrumentation
    try:
        config.dynamic_instrumentation.enabled = True
        print("  ✓ config.dynamic_instrumentation.enabled = True")
        print(f"  ✓ Current value: {config.dynamic_instrumentation.enabled}")
    except AttributeError as e:
        print(f"  ⚠ dynamic_instrumentation not available: {e}")
        
except ImportError as e:
    print(f"✗ Could not import config: {e}")

print()

# Check debugging module
try:
    from ddtrace.debugging import DynamicInstrumentation
    print("✓ ddtrace.debugging.DynamicInstrumentation available")
except ImportError:
    print("⚠ ddtrace.debugging.DynamicInstrumentation not available")
    print("  This is required for Exception Replay")

print()

# Check environment
import os
print("Environment Variables:")
print(f"  DD_TRACE_ENABLED: {os.environ.get('DD_TRACE_ENABLED', 'not set')}")
print(f"  DD_SERVICE: {os.environ.get('DD_SERVICE', 'not set')}")
print(f"  DD_ENV: {os.environ.get('DD_ENV', 'not set')}")
print(f"  DD_VERSION: {os.environ.get('DD_VERSION', 'not set')}")
print(f"  DD_AGENT_HOST: {os.environ.get('DD_AGENT_HOST', 'not set (default: localhost)')}")
print(f"  DD_AGENT_PORT: {os.environ.get('DD_AGENT_PORT', 'not set (default: 8126)')}")
api_key = os.environ.get('DD_API_KEY', 'not set')
if api_key and api_key != 'not set':
    print(f"  DD_API_KEY: {'*' * 20} (set)")
else:
    print(f"  DD_API_KEY: not set")

print()

# Check Datadog Agent
print("Checking Datadog Agent connection...")
try:
    import requests
    agent_host = os.environ.get('DD_AGENT_HOST', 'localhost')
    agent_port = os.environ.get('DD_AGENT_PORT', '8126')
    
    try:
        response = requests.get(f'http://{agent_host}:{agent_port}/info', timeout=2)
        if response.status_code == 200:
            print(f"  ✓ Datadog Agent is running at {agent_host}:{agent_port}")
        else:
            print(f"  ⚠ Datadog Agent responded with status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"  ✗ Cannot connect to Datadog Agent at {agent_host}:{agent_port}")
        print("  → Make sure Datadog Agent is installed and running")
    except requests.exceptions.Timeout:
        print(f"  ✗ Connection to Datadog Agent timed out")
except ImportError:
    print("  ⚠ requests library not installed (optional check)")
    print("  → Install with: pip install requests")

print()
print("=" * 70)
print("Configuration Check Complete")
print("=" * 70)
print()

# Summary
print("Summary:")
print("--------")
try:
    import ddtrace
    from ddtrace import config
    
    if hasattr(config, 'exception_replay'):
        print("✓ Exception Replay feature is available")
        print()
        print("Next steps:")
        print("1. Make sure Datadog Agent is running")
        print("2. Set DD_API_KEY and DD_APP_KEY in .env file")
        print("3. Run: python dollar_checker.py 'test $'")
        print("4. Go to Datadog: APM → Error Tracking")
        print("5. Look for RuntimeError exceptions")
        print("6. Click on error → Look for 'Exception Replay' or 'Variables' tab")
    else:
        print("⚠ Exception Replay feature not available")
        print()
        print("To enable Exception Replay:")
        print("1. Upgrade ddtrace: pip install --upgrade 'ddtrace>=2.0.0'")
        print("2. Re-run this check script")
except Exception as e:
    print(f"✗ Error checking configuration: {e}")
