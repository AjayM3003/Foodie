#!/usr/bin/env python3
"""
🤖 FoodieBot - Complete Enhanced Streamlit Application
Database-Driven Conversational Fast Food System

Features:
- MongoDB Cloud Integration ☁️
- AI-Powered Conversations 🧠
- Real-time Analytics 📊
- Smart Recommendations 🎯
- Interest Score Tracking 📈
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import time
from datetime import datetime, timedelta
import sys
import os

# Add project paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.mongodb_manager import MongoDBManager
from src.mongodb_enhanced_agent import MongoDBEnhancedFoodieBotAgent
from src.ai_service import ai_service

def get_related_products(reference_product, db_manager, exclude_ids=None, limit=4):
    """Get products related/similar to the reference product, excluding specified IDs"""
    if exclude_ids is None:
        exclude_ids = []
    
    try:
        # Strategy 1: Same category, different products
        same_category_products = db_manager.search_products(
            category=reference_product.get('category'),
            limit=limit * 2
        )
        
        # Filter out excluded products
        same_category_products = [
            p for p in same_category_products 
            if p.get('product_id') not in exclude_ids
        ]
        
        # Strategy 2: Similar dietary tags
        dietary_tags = reference_product.get('dietary_tags', [])
        similar_dietary_products = []
        if dietary_tags:
            similar_dietary_products = db_manager.search_products(
                dietary_tags=dietary_tags[:2],  # Use first 2 dietary tags
                limit=limit * 2
            )
            similar_dietary_products = [
                p for p in similar_dietary_products 
                if p.get('product_id') not in exclude_ids
            ]
        
        # Strategy 3: Similar price range (±$3)
        ref_price = reference_product.get('price', 10)
        similar_price_products = db_manager.search_products(
            min_price=max(0, ref_price - 3),
            max_price=ref_price + 3,
            limit=limit * 2
        )
        similar_price_products = [
            p for p in similar_price_products 
            if p.get('product_id') not in exclude_ids
        ]
        
        # Combine and score products
        all_candidates = {}
        
        # Add same category products (highest priority)
        for product in same_category_products:
            product_id = product['product_id']
            if product_id not in all_candidates:
                all_candidates[product_id] = {
                    'product': product,
                    'score': 0.4  # Base score for same category
                }
            else:
                all_candidates[product_id]['score'] += 0.4
        
        # Add similar dietary products
        for product in similar_dietary_products:
            product_id = product['product_id']
            if product_id not in all_candidates:
                all_candidates[product_id] = {
                    'product': product,
                    'score': 0.3  # Base score for similar dietary
                }
            else:
                all_candidates[product_id]['score'] += 0.3
        
        # Add similar price products
        for product in similar_price_products:
            product_id = product['product_id']
            if product_id not in all_candidates:
                all_candidates[product_id] = {
                    'product': product,
                    'score': 0.2  # Base score for similar price
                }
            else:
                all_candidates[product_id]['score'] += 0.2
        
        # Calculate additional similarity scores
        for product_id, data in all_candidates.items():
            product = data['product']
            
            # Spice level similarity (if applicable)
            ref_spice = reference_product.get('spice_level', 0)
            prod_spice = product.get('spice_level', 0)
            spice_diff = abs(ref_spice - prod_spice)
            spice_similarity = max(0, (10 - spice_diff) / 10)
            data['score'] += spice_similarity * 0.1
            
            # Mood tags similarity
            ref_moods = set(reference_product.get('mood_tags', []))
            prod_moods = set(product.get('mood_tags', []))
            mood_overlap = len(ref_moods.intersection(prod_moods))
            if ref_moods or prod_moods:
                mood_similarity = mood_overlap / max(1, len(ref_moods.union(prod_moods)))
                data['score'] += mood_similarity * 0.1
        
        # Sort by score and return top products
        sorted_products = sorted(
            all_candidates.values(),
            key=lambda x: x['score'],
            reverse=True
        )
        
        return [item['product'] for item in sorted_products[:limit]]
    
    except Exception as e:
        print(f"Error getting related products: {e}")
        # Fallback: get popular products excluding the specified IDs
        try:
            fallback_products = db_manager.get_popular_products(limit * 2)
            return [
                p for p in fallback_products 
                if p.get('product_id') not in exclude_ids
            ][:limit]
        except:
            return []

# Configure Streamlit
st.set_page_config(
    page_title="🤖 FoodieBot Enhanced",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #FF6B6B 0%, #4ECDC4 100%);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.status-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 15px;
    margin: 1rem 0;
    text-align: center;
}

.chat-container {
    max-height: 600px;
    overflow-y: auto;
    padding: 1rem;
    border: 2px solid #e0e0e0;
    border-radius: 15px;
    background: #ffffff;
    margin-bottom: 0;
    margin-top: 0 !important;
}

/* Remove white space after chat container */
.element-container {
    margin-bottom: 0;
}

/* Custom input styling to remove extra space */
.stTextInput {
    margin-top: 0.5rem;
    margin-bottom: 0;
}

/* Remove white space under subheaders */
h3 {
    margin-bottom: 0rem !important;
    padding-bottom: 0 !important;
}

.element-container:has(h3) {
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
}

/* Specifically target Streamlit subheader elements */
.stMarkdown h3 {
    margin-bottom: 0rem !important;
    padding-bottom: 0 !important;
}

/* Remove extra space between subheader and container */
.stContainer > div {
    margin-top: 0 !important;
}

/* Additional specific targeting for chat subheader */
div[data-testid="stMarkdownContainer"] h3 {
    margin-bottom: 0rem !important;
    padding-bottom: 0rem !important;
}

/* Target the specific element after subheader */
.element-container + .element-container {
    margin-top: 0rem !important;
    padding-top: 0rem !important;
}

/* Comprehensive chat section styling */
.stMarkdown:has(h3) + div {
    margin-top: 0rem !important;
    padding-top: 0rem !important;
}

/* Remove gap between subheader and following elements */
.element-container:has(.stMarkdown h3) + .element-container {
    margin-top: -1rem !important;
}

/* Streamlit container spacing override */
.stContainer {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
}

/* Block-level container spacing */
where(.st-emotion-cache-1y4p8pa) {
    gap: 0rem !important;
}

.user-message {
    background: #ffffff;
    border: 2px solid #2196F3;
    padding: 1.2rem;
    border-radius: 15px;
    margin: 1rem 0;
    box-shadow: 0 2px 8px rgba(33, 150, 243, 0.1);
    color: #1565C0;
    font-weight: 500;
}

.bot-message {
    background: #f8f9fa;
    border: 2px solid #4CAF50;
    padding: 1.2rem;
    border-radius: 15px;
    margin: 1rem 0;
    box-shadow: 0 2px 8px rgba(76, 175, 80, 0.1);
    color: #2E7D32;
    font-weight: 500;
}

.query-info {
    background: #fff3e0;
    border: 1px solid #ff9800;
    padding: 0.8rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    font-family: 'Courier New', monospace;
    font-size: 0.85rem;
    color: #e65100;
}

.recommendation-card {
    background: linear-gradient(135deg, #ffffff 0%, #f5f5f5 100%);
    border: 2px solid #FF6B6B;
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 4px 12px rgba(255, 107, 107, 0.15);
    transition: all 0.3s ease;
}

.recommendation-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 16px rgba(255, 107, 107, 0.25);
}

.metric-big {
    font-size: 2rem;
    font-weight: bold;
    color: #2196F3;
}

.ai-badge {
    background: linear-gradient(45deg, #FF6B6B 0%, #4ECDC4 100%);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: bold;
    display: inline-block;
    margin: 0.25rem;
}

.interest-score {
    background: linear-gradient(45deg, #4CAF50 0%, #8BC34A 100%);
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 15px;
    font-size: 0.8rem;
    font-weight: bold;
    display: inline-block;
    margin-left: 1rem;
}
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize all session state variables"""
    if 'mongodb_agent' not in st.session_state:
        try:
            st.session_state.mongodb_agent = MongoDBEnhancedFoodieBotAgent()
        except Exception as e:
            st.error(f"Failed to initialize FoodieBot: {e}")
            st.stop()
    
    if 'db_manager' not in st.session_state:
        try:
            st.session_state.db_manager = MongoDBManager()
        except Exception as e:
            st.error(f"Failed to connect to database: {e}")
            st.stop()
    
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    if 'current_conversation_id' not in st.session_state:
        conv_id, greeting = st.session_state.mongodb_agent.start_conversation()
        st.session_state.current_conversation_id = conv_id
        st.session_state.conversation_history.append({
            'sender': 'bot',
            'message': greeting,
            'timestamp': datetime.now(),
            'interest_score': 0
        })
    
    if 'total_recommendations' not in st.session_state:
        st.session_state.total_recommendations = []

# Initialize
initialize_session_state()

# Main Header
st.markdown("""
<div class="main-header">
    <h1>🤖 FoodieBot Enhanced</h1>
    <p>AI-Powered Conversational Food Recommendation System</p>
    <p>🚀 MongoDB Cloud + Gemini AI + Groq Intelligence + Real-time Analytics</p>
</div>
""", unsafe_allow_html=True)

# System Status
col1, col2, col3 = st.columns(3)

# Get system stats
ai_status = st.session_state.mongodb_agent.ai_status
conversation_count = len(st.session_state.conversation_history)

with col1:
    gemini_status = "🟢 Active" if ai_status['gemini_available'] else "🔴 Offline"
    st.markdown(f"""
    <div class="status-card">
        <h4>🧠 Gemini AI</h4>
        <div class="metric-big">{gemini_status}</div>
        <p>Conversations</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    groq_status = "🟢 Active" if ai_status['groq_available'] else "🔴 Offline"
    st.markdown(f"""
    <div class="status-card">
        <h4>⚡ Groq AI</h4>
        <div class="metric-big">{groq_status}</div>
        <p>Intent Analysis</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="status-card">
        <h4>💬 Messages</h4>
        <div class="metric-big">{conversation_count}</div>
        <p>This Session</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🧭 Navigation")
page = st.sidebar.selectbox("Choose Experience", [
    "🤖 AI Chat",
    "📊 Analytics Dashboard", 
    "🍔 Product Explorer",
    "⚙️ System Status"
])

# Main Content
if page == "🤖 AI Chat":
    st.header("🤖 Intelligent Food Conversation")
    
    # Display AI Capabilities
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Chat with FoodieBot")
        
        # Chat Container
        with st.container():
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            
            # Display conversation history
            for msg in st.session_state.conversation_history:
                if msg['sender'] == 'user':
                    st.markdown(f"""
                    <div class="user-message">
                        <strong>👤 You:</strong> {msg['message']}
                        <span class="interest-score">Interest: {msg.get('interest_score', 0):.1f}%</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show query information if available
                    if msg.get('query_info'):
                        st.markdown(f"""
                        <div class="query-info">
                            <strong>🔍 Database Query:</strong> {msg['query_info']}
                        </div>
                        """, unsafe_allow_html=True)
                        
                else:
                    st.markdown(f"""
                    <div class="bot-message">
                        <strong>🤖 FoodieBot:</strong> {msg['message']}
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat Input
        user_input = st.text_input("Type your message here...", key="chat_input")
        
        col_send, col_clear = st.columns([1, 1])
        
        with col_send:
            if st.button("Send 📤", key="send_btn") and user_input:
                # Process message
                with st.spinner("🤖 FoodieBot is thinking..."):
                    response = st.session_state.mongodb_agent.process_message(user_input)
                
                # Build query information string
                query_info_str = ""
                if response.get('ai_intent'):
                    ai_intent = response['ai_intent']
                    query_parts = []
                    if ai_intent.get('dietary_preferences'):
                        query_parts.append(f"dietary_tags: {ai_intent['dietary_preferences']}")
                    if ai_intent.get('budget_mentions'):
                        query_parts.append(f"budget: {ai_intent['budget_mentions']}")
                    if ai_intent.get('food_preferences'):
                        query_parts.append(f"search_text: {ai_intent['food_preferences']}")
                    if query_parts:
                        query_info_str = "; ".join(query_parts)
                
                # Add to conversation history
                st.session_state.conversation_history.append({
                    'sender': 'user',
                    'message': user_input,
                    'timestamp': datetime.now(),
                    'interest_score': response['interest_score'],
                    'query_info': query_info_str if query_info_str else None
                })
                
                st.session_state.conversation_history.append({
                    'sender': 'bot',
                    'message': response['response'],
                    'timestamp': datetime.now(),
                    'interest_score': 0,
                    'recommendations': response.get('recommendations', [])
                })
                
                # Store recommendations
                if response['recommendations']:
                    st.session_state.total_recommendations.extend(response['recommendations'])
                
                st.rerun()
        
        with col_clear:
            if st.button("Clear Chat 🗱️", key="clear_btn"):
                st.session_state.conversation_history = []
                st.session_state.total_recommendations = []
                conv_id, greeting = st.session_state.mongodb_agent.start_conversation()
                st.session_state.current_conversation_id = conv_id
                st.session_state.conversation_history.append({
                    'sender': 'bot',
                    'message': greeting,
                    'timestamp': datetime.now(),
                    'interest_score': 0,
                    'recommendations': []
                })
                st.rerun()
    
    with col2:
        st.subheader("🎯 Related Recommendations")
        
        # Get products shown in recent bot messages to find related items
        shown_products = []
        for msg in reversed(st.session_state.conversation_history):
            if msg['sender'] == 'bot' and msg.get('recommendations'):
                shown_products.extend(msg['recommendations'])
                if len(shown_products) >= 2:  # Get last 2 shown products as reference
                    break
        
        # Get related/similar products (not the same ones shown in chat)
        related_recommendations = []
        if shown_products:
            # Use the most recent product as reference
            reference_product = shown_products[0]
            
            # Get related products based on category and attributes
            related_recommendations = get_related_products(
                reference_product, 
                st.session_state.db_manager,
                exclude_ids=[p.get('product_id') for p in shown_products],
                limit=4
            )
        elif st.session_state.total_recommendations:
            # Fallback: get related to any previously recommended product
            reference_product = st.session_state.total_recommendations[-1]
            related_recommendations = get_related_products(
                reference_product,
                st.session_state.db_manager,
                exclude_ids=[p.get('product_id') for p in st.session_state.total_recommendations[-5:]],
                limit=4
            )
        
        # Display related recommendations
        if related_recommendations:
            # Show 3-4 related recommendations
            display_count = min(len(related_recommendations), 4)
            for i, rec in enumerate(related_recommendations[:display_count], 1):
                st.markdown(f"""
                <div class="recommendation-card">
                    <h4>{rec.get('name', 'Unknown Item')}</h4>
                    <p><strong>${rec.get('price', 0):.2f}</strong> • {rec.get('category', 'Food')}</p>
                    <p style="font-size: 0.9rem; color: #666;">{rec.get('description', 'Delicious food item')[:100]}...</p>
                    <div class="ai-badge">Similar Choice</div>
                    <p style="font-size: 0.8rem; margin-top: 0.5rem;"><strong>Tags:</strong> {', '.join(rec.get('dietary_tags', [])[:3])}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("🤖 Start chatting to get personalized recommendations!")
        
        # Interest Score Progress
        if len(st.session_state.conversation_history) > 1:
            interest_scores = [msg.get('interest_score', 0) 
                             for msg in st.session_state.conversation_history 
                             if msg['sender'] == 'user']
            
            if interest_scores:
                current_score = interest_scores[-1]
                st.metric("📈 Interest Score", f"{current_score:.1f}%")
                
                # Progress bar
                progress = min(current_score / 100, 1.0)
                st.progress(progress)
                
                if current_score >= 80:
                    st.success("🔥 High engagement!")
                elif current_score >= 50:
                    st.warning("👍 Good interest level")
                else:
                    st.info("💭 Building interest...")

elif page == "📊 Analytics Dashboard":
    st.header("📊 Real-time Analytics Dashboard")
    
    # Get analytics data
    try:
        analytics = st.session_state.db_manager.get_analytics_data()
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Products", analytics.get('total_products', db_stats))
        
        with col2:
            st.metric("Conversations", analytics.get('total_conversations', 0))
        
        with col3:
            st.metric("Messages", analytics.get('total_messages', len(st.session_state.conversation_history)))
        
        with col4:
            st.metric("Recommendations", analytics.get('total_recommendations', len(st.session_state.total_recommendations)))
        
        # Interest Score Trend
        if len(st.session_state.conversation_history) > 1:
            st.subheader("📈 Interest Score Progression")
            
            scores_data = []
            for i, msg in enumerate(st.session_state.conversation_history):
                if msg['sender'] == 'user' and msg.get('interest_score'):
                    scores_data.append({
                        'Message': i+1,
                        'Interest Score': msg['interest_score']
                    })
            
            if scores_data:
                df = pd.DataFrame(scores_data)
                fig = px.line(df, x='Message', y='Interest Score', 
                            title="Interest Score Over Time",
                            markers=True)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations by Category
        if st.session_state.total_recommendations:
            st.subheader("🍕 Recommendations by Category")
            
            categories = {}
            for rec in st.session_state.total_recommendations:
                cat = rec.get('category', 'Other')
                categories[cat] = categories.get(cat, 0) + 1
            
            if categories:
                fig = px.pie(values=list(categories.values()), 
                           names=list(categories.keys()),
                           title="Recommendation Distribution")
                st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"Analytics error: {e}")
        st.info("💡 Start a conversation to generate analytics data!")

elif page == "🍔 Product Explorer":
    st.header("🍔 Product Database Explorer")
    
    # Search and Filters
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input("🔍 Search products...")
    
    with col2:
        max_price = st.slider("💰 Max Price", 5, 50, 25, 5)
    
    with col3:
        results_limit = st.selectbox("📊 Show Results", [20, 50, 100, "All"], index=2)
    
    # Category Filter
    categories = st.session_state.db_manager.get_categories()
    selected_category = st.selectbox("📂 Category", ["All"] + categories)
    
    # Dietary Filters
    dietary_options = st.multiselect("🥗 Dietary Preferences", 
                                   ["spicy", "vegetarian", "vegan", "gluten-free", "dairy-free"])
    
    # Search Products
    search_params = {
        'limit': 1000 if results_limit == "All" else results_limit,
        'max_price': max_price
    }
    
    if search_term:
        search_params['search_text'] = search_term
    
    if selected_category != "All":
        search_params['category'] = selected_category
    
    if dietary_options:
        search_params['dietary_tags'] = dietary_options
    
    products = st.session_state.db_manager.search_products(**search_params)
    
    st.subheader(f"Found {len(products)} products")
    
    # Display Products
    for product in products:
        with st.expander(f"{product['name']} - ${product['price']:.2f}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Category:** {product.get('category', 'N/A')}")
                st.write(f"**Price:** ${product.get('price', 0):.2f}")
                st.write(f"**Calories:** {product.get('calories', 'N/A')}")
                st.write(f"**Prep Time:** {product.get('prep_time', 'N/A')}")
            
            with col2:
                st.write(f"**Dietary Tags:** {', '.join(product.get('dietary_tags', []))}")
                st.write(f"**Mood Tags:** {', '.join(product.get('mood_tags', []))}")
                st.write(f"**Spice Level:** {product.get('spice_level', 'N/A')}/10")
                st.write(f"**Popularity:** {product.get('popularity_score', 'N/A')}")
            
            st.write(f"**Description:** {product.get('description', 'No description available')}")

elif page == "⚙️ System Status":
    st.header("⚙️ System Status & Configuration")
    
    # API Status
    st.subheader("🔧 API Services Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🧠 Gemini AI")
        if ai_status['gemini_available']:
            st.success("✅ Connected and operational")
        else:
            st.error("❌ Offline or quota exceeded")
            st.info("💡 Update your API key using: `python update_api_key.py gemini YOUR_KEY`")
    
    with col2:
        st.markdown("### ⚡ Groq AI") 
        if ai_status['groq_available']:
            st.success("✅ Connected and operational")
        else:
            st.error("❌ Offline")
    
    # Database Status
    st.subheader("☁️ MongoDB Status")
    try:
        product_count = st.session_state.db_manager.get_products_count()
        categories = st.session_state.db_manager.get_categories()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Products", product_count)
        
        with col2:
            st.metric("Categories", len(categories))
        
        with col3:
            st.metric("Connection", "✅ Active")
        
        st.success("☁️ MongoDB Cloud is fully operational")
        
    except Exception as e:
        st.error(f"Database connection error: {e}")
    
    # System Information
    st.subheader("🔍 System Information")
    
    system_info = {
        "Python Version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "Streamlit Version": st.__version__,
        "Session Start": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Conversation ID": st.session_state.current_conversation_id,
        "Messages in Session": len(st.session_state.conversation_history)
    }
    
    for key, value in system_info.items():
        st.text(f"{key}: {value}")


# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    🤖 <strong>FoodieBot Enhanced</strong> - AI-Powered Food Recommendations<br>
    Built with Streamlit • MongoDB Cloud • Gemini AI • Groq Intelligence<br>
    <em>Real-time conversational food discovery system</em>
</div>
""", unsafe_allow_html=True)
