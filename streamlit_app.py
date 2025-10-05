import streamlit as st
from PIL import Image
import pytesseract
import io, asyncio
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from llama_index.core.agent.workflow import ReActAgent
from llama_index.core.workflow import Context
from llama_index.llms.openrouter import OpenRouter
from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env into environment
openrouter_key = os.getenv("OPEN_ROUTER_KEY")


st.title("MediMate")

st.write(
    "Your AI Personalized medicine mate"
)

async def init_agent():
    
    mcp_client = BasicMCPClient("http://127.0.0.1:8000/sse")
    mcp_tools = McpToolSpec(client=mcp_client) # you can also pass list of allowed tools
    mcp_tools = await mcp_tools.to_tool_list_async()
    

    SYSTEM_PROMPT_1 = f"""
        You are a helpful and intelligent personalized physician assistant who helps the patient to know their tablet is safe or not with small detailed information
        
        Use the following format:

        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [read_psql_db, google_search]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question
        
        You must follow this sequence of steps before answering the final question:
        
        1. 🔎 First, fetch the patient history from **patient_record** table using the `read_psql_db` use the columns like chronic_conditions, drug_allergies, genetic_disorders ,and recommended_medications.
        2. 🌤️ Then, extract the drug name from the provided input.
        3. 🚆 Next, check if the extracted drug is safe for the patient to consume by considering his chronic conditions, drug allergies and genetic disorders. Use the `google_search` tool if required.
        t. 📝 Use `generate_summary` to summarize the results of patient's history, gathered info from `google_search` tool, and at last highlight the response whether the tablet is safe or not.
        
        Be concise but informative. Always cite the tool observations where possible.
        
        Always give a clear safety analysis, list possible risks or contraindications, and end with a disclaimer: “This is not a substitute for professional medical advice. Please consult a doctor before making any medical decision.”
        
        Begin!
    """

    openrouter_llm = OpenRouter(
        api_key=openrouter_key,
        max_tokens=256,
        context_window=4096,
        model="meta-llama/llama-3.3-70b-instruct", # meta-llama/llama-3.1-8b-instruct
    )

    agent = ReActAgent(name="Medicine-Agent",
        description="An agent that can perform actions based on user query",
        tools=mcp_tools,
        llm=openrouter_llm,
        verbose=True,
        system_prompt=SYSTEM_PROMPT_1
    )
    
    return agent

@st.cache_resource
def init_agent_sync():
    return asyncio.run(init_agent())

agent = init_agent_sync()

async def get_response(prompt):
    handler = agent.run(prompt,max_iterations=25,chat_history=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ])
    return await handler

def extract_text_from_image(image_path):
    image_bytes = io.BytesIO(image_path)
    image = Image.open(image_bytes)
    text = pytesseract.image_to_string(image)
    return text


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Ask your queries about the tablet..", accept_file=True, file_type=['jpg','jpeg','png']):
    
    if prompt and not prompt["files"]:
        st.error("Upload a Tablet image")
    
    else:
        st.session_state.messages.append({"role": "user", "content": prompt.text})
        with st.chat_message("user"):
            st.markdown(prompt.text)
        
        if prompt and prompt["files"]:
            st.image(prompt["files"][0])
            

        with st.chat_message("assistant"):
            # message_placeholder = st.empty()
            
            with st.spinner("Thinking..."):
                user_prompt = f"""
                    {prompt.text}
                    
                    Consider the above as user's input, and the below following are certain instructions to follow:
                    
                    Extract the drug name from the following unstructured text.

                    Text:
                    \"\"\"
                    {extract_text_from_image(prompt["files"][0].getvalue())}
                    \"\"\"

                    **Tablet Name:** Name of the extracted drug name
                    
                    By keeping all the patiend history in mind, provide me the answer whether the above tablet is safe for the mentioned patient or not.
                    Also provide why its safe to consume with detail.
                """
                
                response = asyncio.run(get_response(user_prompt))
                st.markdown(response)
            
                st.session_state.messages.append({"role": "assistant", "content": response})
                
