import streamlit as st
import openai
import PyPDF2
import pandas as pd
import io

# -- Set page config --
st.set_page_config(page_title="Chat with PDF or CSV", layout="centered")

# Sidebar settings
# st.sidebar.title("Chatbot Settings")
import streamlit as st

# Styled header with gear icon
st.sidebar.markdown('<h1 class="sidebar-header-custom">⚙️ Chatbot Settings</h1>', unsafe_allow_html=True)
# theme = st.sidebar.selectbox("Select Theme", ["Light", "Dark"])

# st.markdown("""
#         <style>
#             body {
#                 background-color: #2e2e2e;
#                 color: #f1f1f1;
#             }
#             .stApp {
#                 background-color: #2e2e2e;
#                 color: #f1f1f1;
#             }
#             .stTextInput input {
#                 background-color: #444;
#                 color: #f1f1f1;
#             }
#             .stButton button {
#                 background-color: #444;
#                 color: #f1f1f1;
#             }
#             .stFileUploader input {
#                 background-color: #444;
#                 color: #f1f1f1;
#             }
#             .stTextArea textarea {
#                 background-color: #444;
#                 color: #f1f1f1;
#             }
#             .stMarkdown {
#                 color: #f1f1f1;
#             }
#             .sidebar-header-custom {
#                 background-color: #f1f1f1 !important;
#                 color: #2e2e2e;
#             }
#             .sidebar-header-textbox input{
#                 background-color: white !important;
#                 color: #2e2e2e;
#             }
#             h1 {
#                 color: #f1f1f1;
#             }
#             h4 {
#                 color: #f1f1f1;
#             }
#         </style>
#     """, unsafe_allow_html=True)
st.sidebar.markdown('<h3 class="sidebar-header-custom">Select Theme</h3>', unsafe_allow_html=True)
theme = st.sidebar.selectbox("", ["Dark", "Light"])

# Set CSS based on selected theme
st.markdown("""
            <style>
                .sidebar-header-custom {
                    background-color: #f1f1f1 !important;
                    color: #2e2e2e;
                }
                .sidebar-header-textbox input{
                    background-color: white !important;
                    color: #2e2e2e;
                }
            </style>
            """, unsafe_allow_html=True)
if theme == "Dark":
    st.markdown("""
        <style>
            body {
                background-color: #2e2e2e;
                color: #f1f1f1;
            }
            header {
                background-color: #2e2e2e !important;
            }
            .stApp {
                background-color: #2e2e2e;
                color: #f1f1f1;
            }
            .stTextInput input {
                background-color: #444;
                color: #f1f1f1;
            }
            .stButton {
                text-align: center;    
            }
            .stButton button {
                background-color: #444;
                color: #f1f1f1;
                text-align: center;
            }
            .stFileUploader input {
                background-color: #444;
                color: #f1f1f1;
            }
            .stTextArea textarea {
                background-color: #444;
                color: #f1f1f1;
            }
            .stMarkdown {
                color: #f1f1f1;
            }
            
            h1 {
                color: #f1f1f1;
            }
            h4 {
                color: #f1f1f1;
            }
            .uploadPdf{
                color: #f1f1f1;
                text-align: center;
            }
            div.stChatInput {
                color: #f1f1f1 !important;
                background-color: #2e2e2e !important;
            }
            div.stChatInput textarea {
                color: #f1f1f1;
                background-color: #2e2e2e;
            }
            [data-testid="stBottomBlockContainer"] {
                color: #f1f1f1 !important;
                background-color: #2e2e2e !important;
                width: 730px !important;
            }
            [data-testid="stBottom"] {
                width: 0;
            }
            [data-testid="baseButton-header"]{
                color: black;
            }
            [data-testid="collapsedControl"]{
                color: black;
                background-color: grey;
            }
            [data-testid="stSidebarUserContent"]{
                background-color: #696363;
            }
            [data-testid="stSidebarContent"]{
                background-color: #696363;
            }
            .sidebar-header-custom {
                background-color: #696363 !important;
                color: white;
            }
            .sidebar-header-textbox input{
                background-color: #696363 !important;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

elif theme == "Light":
    st.markdown("""
        <style>
            body {
                background-color: #ffffff;
                color: #2e2e2e;
            }
            .stHeader {
                background-color: #ffffff;    
            }
            .stApp {
                background-color: #ffffff;
                color: #2e2e2e;
            }
            .stTextInput input {
                background-color: #f1f1f1;
                color: #2e2e2e;
            }
            .stButton {
                text-align: center;    
            }
            .stButton button {
                background-color: #f1f1f1;
                color: #2e2e2e;
                text-align: center;
            }
            .stFileUploader input {
                background-color: #f1f1f1;
                color: #2e2e2e;
            }
            .stTextArea textarea {
                background-color: #f1f1f1;
                color: #2e2e2e;
            }
            .stMarkdown {
                color: #2e2e2e;
            }
            h1 {
                color: #2e2e2e;
            }
            h4 {
                color: #2e2e2e;
            }
            .uploadPdf{
                color: #2e2e2e;
                text-align: center;
            }
            div.stChatInput {
                color: #2e2e2e !important;
                background-color: #f1f1f1 !important;
            }
            div.stChatInput textarea {
                color: #2e2e2e;
                background-color: #f1f1f1;
            }
            [data-testid="stBottomBlockContainer"] {
                color: #2e2e2e !important;
                background-color: #f1f1f1 !important;
                width: 730px !important;
            }
            [data-testid="stBottom"] {
                width: 0;
            }
            .sidebar-header-custom {
                background-color: #f1f1f1 !important;
                color: #2e2e2e;
            }
            .sidebar-header-textbox input{
                background-color: white !important;
                color: #2e2e2e;
            }
        </style>
    """, unsafe_allow_html=True)

st.sidebar.markdown('<h2 class="sidebar-header-custom"> Need Help?</h2>', unsafe_allow_html=True)
st.sidebar.markdown('<p class="sidebar-header-custom"> Here are some tips: </p>', unsafe_allow_html=True)
st.sidebar.markdown('<p class="sidebar-header-custom"> - Upload a PDF or CSV file to begin chatting.</p>', unsafe_allow_html=True)
st.sidebar.markdown('<p class="sidebar-header-custom"> - Ask any question related to the file\'s contents.</p>', unsafe_allow_html=True)
st.sidebar.markdown('<p class="sidebar-header-custom"> - Use the \'Clear Chat\' button to reset everything.</p>', unsafe_allow_html=True)
# user_name = st.sidebar.text_input("Your Name", "John")

# Add the "Rate my help" section to the sidebar
st.sidebar.markdown('<h4 style="text-align: center;" class="sidebar-header-custom">Rate my help</h4>', unsafe_allow_html=True)
rating = st.sidebar.slider("", 1, 5, 3, key="rating_slider")
st.sidebar.write(f"Thanks for your feedback! You rated {rating} stars.")
# Styled text label before input
# st.sidebar.markdown('<h3 class="sidebar-header-custom">Enter Your Name:</h3>', unsafe_allow_html=True)
# user_name = st.sidebar.text_input("", "", key="username", label_visibility="collapsed")
# st.sidebar.markdown("---")

# Inject CSS to align the GIF with the heading
# st.markdown("""
#     <style>
#         .header-container {
#             display: flex;
#             align-items: center;
#             gap: 10px; /* Spacing between text and GIF */
#         }
#         .header-container h1 {
#             margin: 0;
#             color: #4CAF50; /* Change text color */
#         }
#         .gif-container img {
#             width: 60px; /* Adjust GIF size */
#             height: auto;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # Display the heading and GIF together using HTML
# st.markdown("""
#     <div class="header-container">
#         <h1>Hi! I am PDFact</h1>
#         <div class="gif-container">
#             <img src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExajdmOTFreXBsZm5ra3l5eWxyaXRkZnhvdXhpb296a3RpMWt6dGhlMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/bSO4PKc7BxdeOMWwnf/giphy.gif" alt="GIF">
#         </div>
#     </div>
# """, unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align: center;'>🤖 Hi! I am PDFact</h1>", unsafe_allow_html=True)
st.write("<h4 style='text-align: center;'> Ask me anything about your pdf! I will get you an answer.", unsafe_allow_html=True)

# E API Key 
OPENAI_API_KEY = ""
openai.api_key = OPENAI_API_KEY  

# **"Clear Chat" Button**: Resets session state
if st.button("Clear Chat & upload new file", key="clear_chat"):
    st.session_state.clear()
    st.rerun()  # Refresh the page to reset everything

# Initialize session state to store messages and file text
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "file_text" not in st.session_state:
    st.session_state["file_text"] = ""

# 📂 File uploader for PDF or CSV
st.markdown('<p class="uploadPdf">📤 Upload a PDF or CSV</p>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["pdf", "csv"])

if uploaded_file is not None:
    file_ext = uploaded_file.name.split(".")[-1].lower()
    
    if file_ext == "pdf":
        # Read PDF file as text
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        all_text = []
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                all_text.append(text)
        st.session_state["file_text"] = "\n".join(all_text)
        st.success("✅ PDF text successfully extracted! You can start chatting now.")
    
    elif file_ext == "csv":
        # Read CSV into DataFrame and convert to text
        df = pd.read_csv(uploaded_file)
        st.session_state["file_text"] = df.to_string(index=False)
        st.success("✅ CSV contents successfully extracted! You can start chatting now.")

# 💬 Display chat messages (Assistant & User)
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 💡 Chat input: only active after we have file text
if st.session_state["file_text"]:
    user_input = st.chat_input("💬 Ask something about the file...")
    if user_input:
        # Add user query to message history
        st.session_state["messages"].append({"role": "user", "content": user_input})

        # Display user message
        with st.chat_message("user"):
            st.write(user_input)

        # 🎯 Prepare system prompt
        system_prompt = (
            "You are a helpful assistant. Use ONLY the following text to answer "
            "the user's question. If the answer is not contained within the text, "
            "say 'I could not find that in the file.'\n\n"
            f"📄 File Contents:\n{st.session_state['file_text']}\n\n"
            "User's question:"
        )

        # 🚀 Call OpenAI API
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input},
                ],
                temperature=0.7,
                max_tokens=512,
            )

            assistant_response = response["choices"][0]["message"]["content"]
        except Exception as e:
            assistant_response = f"❌ Error: {str(e)}"

        # Add assistant response to message history
        st.session_state["messages"].append({"role": "assistant", "content": assistant_response})

        # 📝 Display assistant response
        with st.chat_message("assistant"):
            st.write(assistant_response)