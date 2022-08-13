mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"juanpacualete12@streamlit.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml

echo "\
[theme]\n\
backgroundColor="#e3e3e6"\n\
secondaryBackgroundColor="#a9a9ad"\n\
textColor="#000000"\n\
font="serif"\n\
" > ~/.streamlit/config.toml
