#!/usr/bin/env python3
"""
Streamlit app launcher with SSL certificate workaround for macOS
"""
import os
import sys
import ssl
import certifi

# Set SSL certificate environment variables before importing other modules
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

# Monkey patch SSL context creation to avoid permission errors
original_create_default_context = ssl.create_default_context

def patched_create_default_context(purpose=ssl.Purpose.SERVER_AUTH, *, cafile=None, capath=None, cadata=None):
    """Patched version that uses certifi's certificate bundle"""
    if cafile is None:
        cafile = certifi.where()
    try:
        return original_create_default_context(purpose, cafile=cafile, capath=capath, cadata=cadata)
    except PermissionError:
        # Fallback: create context without verification (not recommended for production)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context

ssl.create_default_context = patched_create_default_context

# Now run streamlit
if __name__ == "__main__":
    from streamlit.web import cli as stcli
    sys.argv = ["streamlit", "run", "app.py"]
    sys.exit(stcli.main())

