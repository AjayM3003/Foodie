# 🚀 MongoDB Enhanced FoodieBot Setup Guide

This guide will help you set up the MongoDB-enhanced FoodieBot system with cloud database integration and AI-powered features.

## 📋 Prerequisites

### Required Software
- Python 3.11 or higher
- Git (optional, for cloning)
- Internet connection for MongoDB Atlas

### Required Accounts
- MongoDB Atlas account (free tier available)
- Google AI API key (for Gemini)
- Groq API key (for advanced analysis)

## 🗄️ MongoDB Cloud Setup

### 1. Create MongoDB Atlas Account
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Sign up for free account
3. Create a new project called "FoodieBot"

### 2. Create Database Cluster
1. Click "Build a Database"
2. Choose "FREE" tier (M0 Sandbox)
3. Select cloud provider and region
4. Name your cluster "FoodieCluster"
5. Click "Create Cluster"

### 3. Configure Database Access
1. Go to "Database Access" tab
2. Click "Add New Database User"
3. Username: `mail2ajay30_db_user`
4. Password: Generate secure password and save it
5. Select "Read and write to any database"
6. Click "Add User"

### 4. Configure Network Access
1. Go to "Network Access" tab
2. Click "Add IP Address"
3. Select "Allow Access from Anywhere" (for development)
4. Click "Confirm"

### 5. Get Connection String
1. Go to "Database" tab
2. Click "Connect" on your cluster
3. Select "Connect your application"
4. Copy the connection string
5. It should look like:
   ```
   mongodb+srv://mail2ajay30_db_user:<password>@foodie.rvp6ixl.mongodb.net/?retryWrites=true&w=majority&appName=Foodie
   ```

## ⚙️ Local Environment Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- `pymongo==4.6.0` - MongoDB driver
- `dnspython==2.4.0` - Required for MongoDB SRV connections
- `streamlit>=1.28.0` - Web interface
- `plotly>=5.17.0` - Data visualization
- `google-generativeai` - Gemini AI
- `groq` - Groq AI
- Plus all existing dependencies

### 2. Configure Environment Variables
Update your `.env` file with MongoDB credentials:

```env
# MongoDB Configuration
MONGODB_URI=mongodb+srv://mail2ajay30_db_user:<db_password>@foodie.rvp6ixl.mongodb.net/?retryWrites=true&w=majority&appName=Foodie
MONGODB_PASSWORD=your_actual_password_here
MONGODB_DATABASE=foodiebot

# AI API Keys (existing)
GEMINI_API_KEY=AIzaSyB2NqoLyGw9pG5QRu6D0K8tn6smxi7WIiA
GROQ_API_KEY=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
```

**Important**: Replace `<db_password>` with your actual MongoDB password and update `MONGODB_PASSWORD` field.

## 🚀 Quick Start

### 1. Test MongoDB Connection
```bash
python database/mongodb_manager.py
```

You should see:
```
✅ Connected to database: foodiebot
📊 Collections: ['products', 'conversations', 'messages', 'recommendations', 'user_preferences', 'analytics_daily']
✅ MongoDB Manager test completed successfully!
```

### 2. Load Initial Data
```bash
python scripts/load_products_mongodb.py
```

This will:
- Connect to MongoDB Atlas
- Generate 100 sample food products
- Create database collections with proper indexes
- Load sample conversation data
- Verify system setup

### 3. Test Enhanced Agent
```bash
python src/mongodb_enhanced_agent.py
```

Expected output:
```
🤖 MongoDB Enhanced FoodieBot Agent Test
🗄️ MongoDB Stored: True
📊 Interest Score: 90.0%
✅ MongoDB Enhanced FoodieBot Agent test complete!
```

### 4. Launch Web Application
```bash
streamlit run mongodb_app.py
```

The enhanced app will launch with:
- ☁️ MongoDB Cloud integration
- 🤖 Gemini AI conversations
- ⚡ Groq AI intent analysis
- 📊 Real-time analytics
- 🔥 Cloud-scale performance

## 📁 Project Structure

```
foodiebot/
├── database/
│   ├── mongodb_manager.py      # MongoDB cloud database manager
│   └── database_manager.py     # Legacy SQLite manager
├── src/
│   ├── mongodb_enhanced_agent.py   # AI + MongoDB agent
│   ├── enhanced_foodie_agent.py    # AI agent (SQLite)
│   ├── ai_service.py               # Gemini + Groq integration
│   └── interest_scorer.py          # Interest scoring engine
├── scripts/
│   └── load_products_mongodb.py    # MongoDB data loader
├── mongodb_app.py              # Enhanced Streamlit app
├── enhanced_app.py             # Standard Streamlit app  
├── requirements.txt            # Dependencies with MongoDB
├── .env                       # Environment configuration
└── README.md                  # Project documentation
```

## 🎯 Features Enabled

### Database Features
- ✅ **MongoDB Atlas Cloud**: Scalable, managed database
- ✅ **Auto-indexing**: Optimized for search and analytics
- ✅ **Real-time Sync**: Instant data updates across sessions
- ✅ **Cloud Backup**: Automatic data protection
- ✅ **Global Scale**: Access from anywhere

### AI Features  
- ✅ **Gemini AI**: Enhanced conversational responses
- ✅ **Groq AI**: Advanced intent analysis
- ✅ **Smart Recommendations**: AI-powered product matching
- ✅ **Context Retention**: Conversation memory across sessions
- ✅ **Intelligent Scoring**: Real-time engagement analysis

### Analytics Features
- ✅ **Real-time Dashboards**: Live conversation analytics
- ✅ **Performance Metrics**: Database and AI performance
- ✅ **Trend Analysis**: Popular products and categories
- ✅ **Export Capabilities**: JSON data export
- ✅ **Cloud Insights**: MongoDB performance monitoring

## 🧪 Testing & Verification

### 1. Database Connection Test
```bash
python -c "
from database.mongodb_manager import MongoDBManager
db = MongoDBManager()
print(f'✅ Connected to: {db.database_name}')
print(f'📦 Products: {db.get_products_count()}')
db.close_connection()
"
```

### 2. AI Integration Test
```bash
python -c "
from src.ai_service import ai_service
status = ai_service.health_check()
print(f'🤖 Gemini: {status[\"gemini_available\"]}')
print(f'⚡ Groq: {status[\"groq_available\"]}')
"
```

### 3. End-to-End Test
```bash
python -c "
from src.mongodb_enhanced_agent import MongoDBEnhancedFoodieBotAgent
agent = MongoDBEnhancedFoodieBotAgent()
conv_id, greeting = agent.start_conversation()
response = agent.process_message('I want spicy food under \$15')
print(f'✅ Response: {response[\"response\"][:50]}...')
print(f'📊 Interest: {response[\"interest_score\"]}%')
print(f'🗄️ MongoDB: {response[\"mongodb_stored\"]}')
agent.close_database_connection()
"
```

## 🔧 Troubleshooting

### MongoDB Connection Issues

**Problem**: `ServerSelectionTimeoutError`
```python
pymongo.errors.ServerSelectionTimeoutError: connection closed
```

**Solution**:
1. Check internet connection
2. Verify MongoDB password in `.env` file
3. Ensure IP is whitelisted in MongoDB Atlas
4. Check cluster status in MongoDB Atlas dashboard

**Problem**: `Authentication failed`
```python
pymongo.errors.OperationFailure: Authentication failed
```

**Solution**:
1. Verify username: `mail2ajay30_db_user`
2. Check password matches MongoDB Atlas user
3. Ensure user has "Read and write" permissions

### AI Service Issues

**Problem**: Gemini API errors
```python
google.generativeai.types.generation_types.BlockedPromptException
```

**Solution**:
1. Check `GEMINI_API_KEY` in `.env` file
2. Verify API key has proper permissions
3. Check API quota limits

**Problem**: Groq API errors  
```python
groq.APIError: Bad Request
```

**Solution**:
1. Check `GROQ_API_KEY` in `.env` file
2. Verify API key format
3. Check rate limits

### Performance Issues

**Problem**: Slow database queries
```python
# Query takes > 1000ms
```

**Solution**:
1. Check MongoDB Atlas cluster tier
2. Review query patterns in application logs
3. Consider upgrading cluster for better performance
4. Use indexes for frequently queried fields

## 📊 Performance Optimization

### Database Optimization
- **Indexes**: Automatically created for common queries
- **Aggregation**: Complex analytics use MongoDB pipelines
- **Connection Pooling**: Optimized connection management
- **Query Optimization**: Efficient search and filter operations

### AI Optimization
- **Caching**: AI responses cached for similar queries
- **Fallback Logic**: Graceful degradation when APIs unavailable
- **Batch Processing**: Efficient handling of multiple requests
- **Error Recovery**: Automatic retry mechanisms

## 🚀 Deployment Options

### Local Development
```bash
# Run locally with MongoDB Atlas
streamlit run mongodb_app.py
```

### Cloud Deployment (Streamlit Cloud)
1. Push code to GitHub repository
2. Connect to Streamlit Cloud
3. Add environment variables in Streamlit Cloud settings
4. Deploy with one click

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "mongodb_app.py"]
```

## 📈 Monitoring & Analytics

### MongoDB Atlas Monitoring
- Database performance metrics
- Connection statistics
- Query performance analysis
- Storage usage tracking

### Application Monitoring  
- Real-time conversation analytics
- AI service performance metrics
- User engagement tracking
- System health dashboards

## 🔐 Security Best Practices

### Database Security
- ✅ Use strong passwords
- ✅ Enable IP whitelisting
- ✅ Regular access reviews
- ✅ Monitor connection logs

### API Security
- ✅ Keep API keys secure
- ✅ Use environment variables
- ✅ Regular key rotation
- ✅ Monitor usage quotas

### Application Security
- ✅ Input validation
- ✅ Error handling
- ✅ Logging security events
- ✅ Regular updates

## 📞 Support & Resources

### MongoDB Resources
- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)
- [MongoDB University](https://university.mongodb.com/)
- [Community Forums](https://developer.mongodb.com/community/forums/)

### AI Service Resources  
- [Google AI Documentation](https://ai.google.dev/)
- [Groq Documentation](https://groq.com/docs/)
- [OpenAI Best Practices](https://platform.openai.com/docs/guides/best-practices)

### Project Resources
- GitHub Issues: Report bugs and feature requests
- Documentation: Comprehensive setup and usage guides
- Examples: Sample implementations and use cases

## 🎉 Success Checklist

- ✅ MongoDB Atlas cluster created and configured
- ✅ Database user created with proper permissions
- ✅ Connection string configured in `.env` file
- ✅ Python dependencies installed successfully
- ✅ MongoDB manager test passes
- ✅ AI services configured and tested
- ✅ Sample data loaded into database
- ✅ Enhanced agent test passes
- ✅ Web application launches successfully
- ✅ All features working as expected

## 🔄 Next Steps

1. **Customize Data**: Add your own product catalog
2. **Enhance AI**: Train with domain-specific data
3. **Scale Up**: Upgrade MongoDB cluster as needed
4. **Monitor Usage**: Set up alerts and monitoring
5. **Deploy Production**: Move to production environment

---

🎯 **Ready to Launch!** Your MongoDB-enhanced FoodieBot is now configured for cloud-scale operations with AI intelligence. The system provides enterprise-grade database performance, advanced AI capabilities, and real-time analytics for superior food recommendation experiences.

For questions or issues, check the troubleshooting section or refer to the comprehensive documentation provided.
