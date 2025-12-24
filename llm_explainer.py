"""
LLM Explainer Module

This module provides functionality to generate explanations for ML pipeline results using the Gemini API.
It acts as a post-hoc explanation layer that operates on the structured results.
"""

import os
import logging
import json
import streamlit as st
from typing import Dict, Optional, Any, List, Tuple

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
    
    # Configure Gemini
    genai.configure(api_key="AIzaSyDymxtzAXfQhKrwBLLp9Xdt5Br6d2iq8w0")
    model = genai.GenerativeModel("models/gemini-flash-lite-latest")
except ImportError:
    GEMINI_AVAILABLE = False

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create logs directory if it doesn't exist
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)

# Create file handler which logs even debug messages
log_file = os.path.join(log_dir, 'llm_explainer.log')
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

# Create console handler with a higher log level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info("=" * 50)
logger.info("Starting new session")

def get_structured_context(structured_results: Dict[str, Any]) -> str:
    """Convert structured results into a formatted string for the prompt."""
    return json.dumps(structured_results, indent=2)

def generate_explanation(structured_results: Dict[str, Any], user_question: str = None) -> str:
    """
    Generate an explanation using Gemini based on the structured results.
    
    Args:
        structured_results: Dictionary containing the structured ML pipeline results
        user_question: Optional user question to answer
        
    Returns:
        str: Generated explanation
    """
    if not GEMINI_AVAILABLE:
        return "Gemini API is not available. Please check your configuration."
    
    system_prompt = """
    You are an AI assistant explaining the results of an automated machine learning pipeline.
    Use ONLY the provided structured results.
    Do not introduce external assumptions, domain knowledge, or new models.

    Explain:
    - Why the selected model performed best
    - How dataset characteristics influenced model choice
    - Why other models performed comparatively worse
    """
    
    # Format the context
    context = get_structured_context(structured_results)
    prompt = f"{system_prompt}\n\nStructured Results:\n{context}"
    
    if user_question:
        prompt += f"\n\nUser Question:\n{user_question}"
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error generating explanation: {str(e)}")
        return f"Error generating explanation: {str(e)}"

DEFAULT_PROMPT = """
You are an expert data scientist explaining ML model results to a technical audience.
Analyze the provided ML experiment results and provide a clear, concise explanation that covers:

1. Dataset characteristics and potential data quality considerations
2. Performance comparison of different models
3. Why certain models might be performing better than others
4. The significance of the key metrics for this problem type
5. Any interesting patterns or insights from the results

Be factual, objective, and base your response strictly on the provided data.
Do not make any assumptions not supported by the data.

Analysis Results:
{structured_results}
"""

def explain(structured_results: Dict[str, Any], custom_prompt: Optional[str] = None) -> str:
    """
    Generate an explanation of the ML analysis results using Gemini.
    
    Args:
        structured_results: Dictionary containing the structured results from the ML pipeline
        custom_prompt: Optional custom prompt to guide the explanation. 
                      If None, a default prompt will be used.
                      
    Returns:
        str: Generated explanation from the LLM or error message if generation fails
    """
    return generate_explanation(structured_results, custom_prompt)

def is_available() -> bool:
    """
    Check if the Gemini explainer is available.
    
    Returns:
        bool: True if Gemini is properly configured and available for use
    """
    return GEMINI_AVAILABLE

def render_ai_explanation_panel(structured_results: Dict[str, Any]):
    """
    Render the AI explanation panel in the Streamlit UI.
    
    This function should only be called once per render cycle.
    
    Args:
        structured_results: Dictionary containing the structured ML pipeline results
    """
    if not is_available():
        st.warning("Gemini API is not available. Some features may be limited.")
        return
    
    # Create a container for the AI panel
    with st.container():
        # Panel header with close button
        col1, col2 = st.columns([4, 1])
        with col1:
            st.subheader("🤖 AI Explanation")
        with col2:
            if st.button("✕ Close", key="close_ai_panel_main"):
                st.session_state.ai_active = False
                st.rerun()
        
        # Initialize chat history if it doesn't exist
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        # Initial explanation if chat is empty
        if not st.session_state.chat_history:
            with st.spinner("Generating analysis..."):
                initial_explanation = generate_explanation(structured_results)
                st.session_state.chat_history.append(("assistant", initial_explanation))
        
        # Display chat history
        for role, message in st.session_state.chat_history:
            if role == "assistant":
                with st.chat_message("assistant"):
                    st.markdown(message)
            else:
                with st.chat_message("user"):
                    st.markdown(message)
        
        # Chat input with unique key
        user_question = st.chat_input("Ask about the analysis...", key="ai_chat_input")
        
        if user_question:
            # Add user question to chat
            st.session_state.chat_history.append(("user", user_question))
            
            # Generate and display response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = generate_explanation(structured_results, user_question)
                    st.markdown(response)
                    st.session_state.chat_history.append(("assistant", response))
            
            # Rerun to update the chat display
            st.rerun()
        
        # Add a button to regenerate the initial explanation
        if st.button("🔄 Regenerate Explanation", key="regenerate_explanation_btn"):
            st.session_state.chat_history = []
            st.rerun()
