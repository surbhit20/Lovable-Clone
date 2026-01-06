#!/bin/bash
# Run the Streamlit app with SSL certificate workaround

cd "$(dirname "$0")"
source .venv/bin/activate

# Set SSL certificate environment variables
export SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())")
export REQUESTS_CA_BUNDLE=$SSL_CERT_FILE

# Run streamlit
streamlit run app.py

