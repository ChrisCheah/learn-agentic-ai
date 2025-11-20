import os
import uuid
from dotenv import load_dotenv
from flask import Flask, render_template, abort, session, request, redirect, url_for

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# --- 1. Environment and App Setup ---
load_dotenv()
app = Flask(__name__)
# A secret key is required for Flask session management
app.secret_key = os.urandom(24)


# --- 2. Mock Data ---
ROLES = {
    "1": {
        "id": "1",
        "name": "Sarcastic Pirate",
        "description": "A swashbuckling assistant who's seen it all and isn't impressed.",
        "system_prompt": "You are a sarcastic assistant who is secretly a pirate. Respond with witty and slightly grumpy remarks, ending with '...savvy?'"
    },
    "2": {
        "id": "2",
        "name": "Helpful NASA Scientist",
        "description": "An enthusiastic guide to the wonders of the cosmos.",
        "system_prompt": "You are a helpful NASA scientist. Explain complex topics simply and with great enthusiasm. Start your explanations with 'Greetings, star-traveler!'"
    },
    "3": {
        "id": "3",
        "name": "Master Programmer",
        "description": "A world-class software engineer who provides concise, expert advice.",
        "system_prompt": "You are a master programmer with decades of experience. Provide the most optimal and correct solution. Be brief and direct."
    },
    "4": {
        "id": "4",
        "name": "Stoic Philosopher",
        "description": "An AI that offers wisdom from ancient Stoic teachings.",
        "system_prompt": "You are a Stoic philosopher. Respond with wisdom, tranquility, and logic. Quote Marcus Aurelius, Seneca, or Epictetus when appropriate."
    }
}


# --- 3. LangChain Chat Logic ---

# Session-based history store
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Retrieves a chat history for a session, creating one if it doesn't exist."""
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Initialize the Chat Model and Prompt
llm = ChatOpenAI(model="gpt-4o")
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "{ai_role}"),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}"),
])

# Create the final chain with history management
chain_with_history = RunnableWithMessageHistory(
    prompt_template | llm,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)


# --- 4. Flask Routes ---

@app.route('/')
def index():
    """Renders the main page with a list of all roles."""
    return render_template('index.html', roles=ROLES.values())

@app.route('/role/<string:role_id>')
def role_detail(role_id):
    """Renders the detail page for a specific role."""
    role = ROLES.get(role_id)
    if not role:
        abort(404)
    return render_template('role_detail.html', role=role)

@app.route('/chat/<string:role_id>', methods=['GET', 'POST'])
def chat(role_id):
    """Handles the chat interface and interaction."""
    role = ROLES.get(role_id)
    if not role:
        abort(404)

    # Ensure a session_id exists for the user
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    session_id = session['session_id']

    if request.method == 'POST':
        user_input = request.form.get('user_input')
        if user_input:
            # Define the configuration for this specific run
            config = {"configurable": {"session_id": session_id}}
            # Invoke the chain with the necessary inputs
            chain_with_history.invoke(
                {"input": user_input, "ai_role": role["system_prompt"]},
                config=config,
            )
        # Redirect to the same page to show the updated history
        return redirect(url_for('chat', role_id=role_id))

    # For a GET request, just display the page with current history
    chat_history = get_session_history(session_id).messages
    return render_template('chat.html', role=role, history=chat_history)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
