#!/usr/bin/env python3
"""
Dollar Sign Checker with Datadog APM Exception Replay
Throws unhandled RuntimeError when $ character is detected
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Datadog APM imports with exception replay
from ddtrace import tracer, patch_all, config
import datadog

# Patch all supported libraries FIRST
patch_all()

# Initialize Datadog
DD_TRACE_ENABLED = os.environ.get('DD_TRACE_ENABLED', 'true').lower() == 'true'

if DD_TRACE_ENABLED:
    # Configure tracer with exception debugging enabled
    tracer.configure(
        hostname=os.environ.get('DD_AGENT_HOST', 'localhost'),
        port=int(os.environ.get('DD_AGENT_PORT', 8126)),
    )
    
    # Enable exception replay (requires ddtrace >= 1.10.0)
    try:
        from ddtrace.debugging import DynamicInstrumentation
        config.exception_replay.enabled = True
        config.dynamic_instrumentation.enabled = True
        print("✓ Exception Replay enabled")
    except (ImportError, AttributeError):
        print("⚠ Exception Replay not available (requires ddtrace >= 1.10.0)")
        print("  Install with: pip install --upgrade ddtrace")
    
    datadog.initialize(
        api_key=os.environ.get('DD_API_KEY'),
        app_key=os.environ.get('DD_APP_KEY'),
    )
    
    print("✓ Datadog APM initialized\n")

@tracer.wrap(service='dollar-checker', resource='check_for_dollar')
def check_for_dollar(text):
    """
    Check text for dollar sign ($).
    Throws unhandled RuntimeError if $ is found.
    
    Args:
        text (str): Text to check
        
    Raises:
        RuntimeError: If $ character is found (UNHANDLED)
    """
    print(f"🔍 Checking text: '{text}'")
    
    # Add trace tags for better debugging
    span = tracer.current_span()
    if span:
        span.set_tag('app.name', 'dollar-checker')
        span.set_tag('input.text', text)
        span.set_tag('input.length', len(text))
        span.set_tag('check.character', '$')
    
    # Check each character
    for i, char in enumerate(text):
        if char == '$':
            # Found dollar sign!
            print(f"\n❌ DOLLAR SIGN DETECTED at position {i}!")
            print(f"   Character: '{char}'")
            print(f"   Position: {i}")
            print(f"   Context: ...{text[max(0,i-5):i+6]}...")
            print(f"\n💥 Throwing unhandled RuntimeError exception...\n")
            
            # Track in Datadog before throwing
            if DD_TRACE_ENABLED:
                datadog.statsd.increment(
                    'dollar_checker.dollar_found',
                    tags=[
                        f'position:{i}',
                        'status:error',
                        'exception:RuntimeError'
                    ]
                )
                
                # Add detailed error tags for exception replay
                if span:
                    span.set_tag('error', True)
                    span.set_tag('error.type', 'RuntimeError')
                    span.set_tag('error.message', f'Dollar sign found at position {i}')
                    span.set_tag('dollar.found', True)
                    span.set_tag('dollar.position', i)
                    span.set_tag('dollar.context', text[max(0,i-5):i+6])
                    
                    # Add custom metadata for exception replay
                    span.set_tag('debug.input_text', text)
                    span.set_tag('debug.character_index', i)
                    span.set_tag('debug.before_context', text[:i])
                    span.set_tag('debug.after_context', text[i+1:])
            
            # THROW UNHANDLED EXCEPTION - Script will crash!
            raise RuntimeError(f"Dollar sign ($) detected at position {i} in text: '{text}'")
    
    # No dollar sign found - success!
    print(f"✅ No dollar sign found - text is valid!\n")
    
    if DD_TRACE_ENABLED:
        datadog.statsd.increment('dollar_checker.success')
        if span:
            span.set_tag('dollar.found', False)
            span.set_tag('validation.passed', True)
    
    return True

@tracer.wrap(service='dollar-checker', resource='main')
def main():
    """Main function"""
    print("=" * 70)
    print("Dollar Sign Checker with Datadog APM Exception Replay")
    print("=" * 70)
    print()
    
    # Check arguments
    if len(sys.argv) < 2:
        print("❌ Error: No text provided\n")
        print("Usage: python dollar_checker.py <text>")
        print("\nExamples:")
        print("  python dollar_checker.py 'Hello World'        # ✅ OK")
        print("  python dollar_checker.py 'Price: 50 dollars'  # ✅ OK")
        print("  python dollar_checker.py 'Price: $50'         # 💥 CRASH!")
        print("  python dollar_checker.py 'Cost is $100'       # 💥 CRASH!")
        print()
        
        if DD_TRACE_ENABLED:
            datadog.statsd.increment('dollar_checker.no_input')
        
        sys.exit(1)
    
    # Get text from command line
    text = ' '.join(sys.argv[1:])
    
    # Track app start
    if DD_TRACE_ENABLED:
        datadog.statsd.increment('dollar_checker.started')
        
        span = tracer.current_span()
        if span:
            span.set_tag('app.version', '1.0.0')
            span.set_tag('app.environment', os.environ.get('DD_ENV', 'development'))
    
    # Check for dollar sign - will throw exception if found
    check_for_dollar(text)
    
    # Success
    print("=" * 70)
    print("✅ SUCCESS - No dollar signs detected!")
    print("=" * 70)
    print()
    
    return 0

if __name__ == '__main__':
    # Run main - exceptions will propagate and crash the script
    exit_code = main()
    sys.exit(exit_code)
